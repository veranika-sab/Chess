import math
from django.db import models
from django.db.models.aggregates import Max


class Player(models.Model):
    name = models.CharField(max_length=300)
    elo_rating = models.IntegerField()

    def __unicode__(self):
        return self.name


class Tournament(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300)
    players = models.ManyToManyField(Player)
    prizes_amount = models.IntegerField(
        help_text="Should be less than players amount and greater than 0"
    )
    tours_amount = models.IntegerField(
        blank=True,
        null=True,
        help_text="The value is counted automatically (depends on players and prizes amount)"
    )
    is_finished = models.BooleanField(
        default=False,
        help_text="The value is changed automatically when all tournament matches are played"
    )

    def __unicode__(self):
        return self.name

    def generate_and_save_tours_amount(self):
        tournament = Tournament.objects.get(id=self.id)
        if not tournament.tours_amount:
            if self.prizes_amount > 1:
                tournament.tours_amount = math.log(self.players.count())/math.log(2) + \
                                          math.log(self.prizes_amount-1)/math.log(2)
            else:
                tournament.tours_amount = int(round(math.log(self.players.count())/math.log(2)))
            tournament.save()

    def create_pairs_for_next_tour(self):
        self.save_data_to_db(*self.generate_pairs(*self.prepare_data_for_pair_generation()))

    def prepare_data_for_pair_generation(self):
        players_elo_ratings = dict(self.players.filter().values_list('id', 'elo_rating', ))
        current_tour = Tour.objects.filter(tournament=self.id).aggregate(Max('tour')).get('tour__max')
        if not current_tour:
            current_tour = 0
        tour_for_generation = current_tour + 1
        all_players_ids_in_tournament = Tournament.objects.filter(id=self.id).values_list('players__id')

        players_ids_and_points_in_tournament_all = \
            list(MatchResult.objects.filter(tournament_tour__in=Tour.objects.filter
                (tournament=self)).values_list('player_one', 'player_one_result')) +\
            list(MatchResult.objects.filter(tournament_tour__in=Tour.objects.filter
                (tournament=self)).values_list('player_two', 'player_two_result'))
        players_ids_and_points_in_tournament = {id[0]: 0 for id in all_players_ids_in_tournament}

        for id_and_point in players_ids_and_points_in_tournament_all:  # count points in tournament for each user
            players_ids_and_points_in_tournament[id_and_point[0]] += id_and_point[1]
        return players_elo_ratings, players_ids_and_points_in_tournament, tour_for_generation

    def generate_pairs(self, players_elo_ratings, players_ids_and_points_in_tournament, tour_for_generation):
        points_group_list = sorted(set(players_ids_and_points_in_tournament.values()), reverse=True)
        players_list_grouped_by_points = [[] for group in points_group_list] # create empty lists for point groups

        for player_id, player_points in players_ids_and_points_in_tournament.items(): # add players to groups
            players_list_grouped_by_points[points_group_list.index(player_points)].append(player_id)
        for index, point_group in enumerate(players_list_grouped_by_points): # sort players in point groups
            point_group.sort(key = lambda x: players_elo_ratings[x], reverse=True)
            if len(point_group) % 2 == 1: # move player to lower point group if odd number of players
                if index+1 < len(players_list_grouped_by_points):
                    players_list_grouped_by_points[index+1].append(point_group.pop())
                else:
                    point_group.append(None)
        pairs = []
        for point_group in players_list_grouped_by_points:
            pairs = self.compose_pairs(pairs, point_group)
        return pairs, tour_for_generation

    def compose_pairs(self, pairs, point_group):
        while point_group:
            current_player = point_group[-1]
            point_group = point_group[:-1]
            point_group.sort()
            for partner in point_group:
                if partner not in self.get_all_partners_for_player(current_player, self.id):
                    pair = [current_player, point_group.pop(point_group.index(partner))]
                    pairs.append(pair)
                    break
                else:
                    if len(point_group)==1:
                        pair = [current_player, point_group.pop()]
                        pairs.append(pair)
        return pairs

    def get_all_partners_for_player(self, player_id, tournament_id): # returns the list of partners for player during the tournament
        partners = set(list(MatchResult.objects.filter(tournament_tour__tournament_id=
                            tournament_id, player_two_id=player_id).values_list('player_one__id', flat=True)) +\
                       list(MatchResult.objects.filter(tournament_tour__tournament_id=
                            tournament_id, player_one_id=player_id).values_list('player_two__id', flat=True)))
        return [partner for partner in partners]


    def save_data_to_db(self, pairs, tour_for_generation):
        next_tour = Tour(tournament=self, tour=tour_for_generation)
        next_tour.save()
        match_results_list = []
        for player_one, player_two in pairs:
            match_results_list.append(MatchResult(tournament_tour=next_tour,
                player_one=Player(id=player_one), player_two=Player(id=player_two)))
        MatchResult.objects.bulk_create(match_results_list)

    def get_pairs_for_all_tours(self):
        all_tournament_results = list(
            MatchResult.objects.filter(tournament_tour__in=Tour.objects.filter(tournament=self)).values_list(
                'tournament_tour__tour', 'player_one__name', 'player_one_result', 'player_two__name', 'player_two_result'
            )
        )
        return all_tournament_results

    def get_active_tours_amount(self):
        return Tour.objects.filter(tournament=self, matchresult__isnull=False).aggregate(Max('tour'))['tour__max']


class Tour(models.Model):
    tournament = models.ForeignKey(Tournament)
    tour = models.IntegerField()

#    def is_tour_finished(self): # delete it?
#        if self.objects.filter(matchresult__player_one_result = -1).exists():
#            print 'no'
#        else:
#            print 'yes'

    def __unicode__(self):
        return u'%s, tour: %s' %(self.tournament, self.tour)

class MatchResult(models.Model):
    tournament_tour = models.ForeignKey(Tour)
    player_one = models.ForeignKey(Player, related_name='Player')
    results = (
        (-1.0, 'No game'),
        (0.0, 'Defeat'),
        (0.5, 'Draw'),
        (1.0, 'Victory'),
        )
    player_one_result = models.FloatField(
        choices=results, default=-1.0, help_text='Define the match result for Player one',
    )
    player_two = models.ForeignKey(Player, related_name='Player competitor',)
    player_two_result = models.FloatField(
        choices=results, default=-1.0, help_text='Define the match result for Player two',
    )

    def check_tournament_status(self):
        is_tour_the_last = self.tournament_tour.tour == self.tournament_tour.tournament.tours_amount
        if not is_tour_the_last:
            return
        if MatchResult.objects.filter(tournament_tour=self.tournament_tour, player_one_result = -1).exists():
            return
        self.tournament_tour.tournament.is_finished = True
        self.tournament_tour.tournament.save()