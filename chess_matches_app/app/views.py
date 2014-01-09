from braces.views import AjaxResponseMixin, JSONResponseMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.aggregates import Sum
from django.shortcuts import render_to_response
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from models import Tournament, Player, MatchResult

class TournamentListView(ListView, AjaxResponseMixin):
    paginate_by = 10
    model = Tournament


class TournamentListAjaxView(ListView, JSONResponseMixin):
    paginate_by = 10
    content_type = "application/json"
    model = Tournament

    def render_to_response(self, context, **response_kwargs):
        context_dict = []
        for tournament in context['object_list']:
            context_dict.append(
                [tournament.id, tournament.name, tournament.players.count(),
                 tournament.prizes_amount,tournament.tours_amount, tournament.is_finished]
            )
        return self.render_json_response(context_dict)


class TournamentDetailView(DetailView):
    model=Tournament
    pk_url_kwarg='tournament_id'

    def get_context_data(self, **kwargs):
        tours_list = range(1, self.object.get_active_tours_amount()+1)
        players_one_all = dict(MatchResult.objects.filter(tournament_tour__tournament=
                            self.object).values_list('player_one__id').annotate(Sum('player_one_result')))
        players_two_all = dict(MatchResult.objects.filter(tournament_tour__tournament=
                            self.object).values_list('player_two__id').annotate(Sum('player_two_result')))
        ids_and_points_dict = players_one_all # start join two queries with players into one dict
        for id, points in players_two_all.items():
            ids_and_points_dict[id] = ids_and_points_dict.setdefault(id, 0) + points

        final_results_list = [          # create final results list with id and name
            [player.id, player.name] for player in self.object.players.all().filter(id__in=ids_and_points_dict)
        ]

        for id_and_name in final_results_list: # add points to final list and delete id
            id_and_name.append(ids_and_points_dict[id_and_name.pop(0)])

        final_results_list = sorted(final_results_list, key=lambda x: x[1], reverse=True) # sort by points desc
        return {
            'tournament': self.object,
            'tournament_results': self.object.get_pairs_for_all_tours(),
            'tours_list': tours_list,
            'final_results_list': final_results_list,
        }


class PlayerListView(ListView):
    paginate_by = 10
    model = Player


class PlayerListAjaxView(ListView, JSONResponseMixin):
    paginate_by = 10
    content_type = "application/json"
    model = Player

    def render_to_response(self, context, **response_kwargs):
        context_dict = []
        for player in context['object_list']:
            context_dict.append(
                [player.id, player.name, player.elo_rating]
            )
        return self.render_json_response(context_dict)
