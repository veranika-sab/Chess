from django.conf.urls import patterns, include, url
from django.contrib import admin
from app.views import TournamentListView
from app.models import Tournament
from app.views import TournamentDetailView
from django.views.generic.detail import DetailView
from app.views import TournamentListAjaxView
from app.views import PlayerListView
from app.views import PlayerListAjaxView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tournaments/$', TournamentListView.as_view(), name="tournaments"),
    url(r'^tournaments/ajax/$', TournamentListAjaxView.as_view(), name="tournaments_ajax"),
    url(r'^tournaments/(?P<tournament_id>\d+)$', TournamentDetailView.as_view(), name="tournament_detail"),
    url(r'^players/', PlayerListView.as_view(), name="players"),
    url(r'^players/ajax/$', PlayerListAjaxView.as_view(), name="players_ajax"),
)

