from django.contrib import admin
from django.contrib.admin.filters import SimpleListFilter
from django.http.response import HttpResponseRedirect
from forms import TournamentAdminForm
from models import Player, Tournament, MatchResult


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'elo_rating')


class TournamentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'prizes_amount', 'tours_amount', 'is_finished')
    filter_horizontal=('players',)
    readonly_fields=('tours_amount', 'is_finished',)
    list_display_links = ('id', 'name', 'prizes_amount', 'tours_amount')
    search_fields = ('name',)
    list_per_page = 20
    form = TournamentAdminForm

    def response_change(self, request, obj):
        if '_generatepairs' in request.POST:
            obj.create_pairs_for_next_tour()
        return HttpResponseRedirect('')

    def save_model(self, request, obj, form, change):
        obj.save()
        form.save_m2m()
        obj.generate_and_save_tours_amount()
        if not change:
            obj.create_pairs_for_next_tour()

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('players', 'prizes_amount',)
        return self.readonly_fields


class TournamentFilter(SimpleListFilter):
    title = 'tournament name'
    parameter_name = 'id'

    def lookups(self, request, model_admin):
        return Tournament.objects.all().values_list('id', 'name').order_by('id')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(tournament_tour__tournament_id__exact=self.value())
        else:
            return queryset


class MatchResultAdmin(admin.ModelAdmin):
    list_display = ('tournament_tour', 'player_one', 'player_one_result',
                    'player_two', 'player_two_result')
    list_display_links = ('tournament_tour', 'player_one', 'player_one_result',
                          'player_two', 'player_two_result')
    list_filter = (TournamentFilter,)

    def save_model(self, request, obj, form, change):
        obj.save()
        form.save_m2m()
        obj.check_tournament_status()

    def has_add_permission(self, request):
        return False

#    def has_delete_permission(self, request, obj=None):
#        return False


admin.site.register(Player, PlayerAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(MatchResult, MatchResultAdmin)