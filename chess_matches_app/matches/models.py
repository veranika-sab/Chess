from django.db import models

# Create your models here.
class Players(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300)
    elo_rating = models.IntegerField(min_value=0, max_value = 3000)


class Matches(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(min_length=1, max_length=300)
    players = models.ManyToManyField(Players)
    prizes = models.IntegerField(min_value=1, max_value=100)
    tours_quantity = models.IntegerField(min_value=1, blank=True)
    is_finished = models.BooleanField(default=0)


class Match_result_types():
    DEFEAT = 0
    DRAW = 0.5
    VICTORY = 1
    UNKNOWN = -1


class Matches_results(models.Model):
    match = models.ForeignKey(Matches)
    tour = models.IntegerField(min_value=1, max_value=100)
    player_1 = models.ForeignKey(Players)
    player_1_points = models.DecimalField(min_digits=0, max_digits=200)
    player_1_tour_result = models.DecimalField(choices=Match_result_types, min_digits=-1, max_digits=1,
                                                default=Match_result_types.UNKNOWN)
    player_1_place = models.IntegerField(min_value=1, blank=True)
    player_2 = models.ForeignKey(Players)
    player_2_points = models.DecimalField(min_digits=0, max_digits=200)
    player_2_tour_result = models.DecimalField(choices=Match_result_types, min_digits=-1, max_digits=1,
                                                 default=Match_result_types.UNKNOWN)
    player_2_place = models.IntegerField(min_value=1, blank=True)

