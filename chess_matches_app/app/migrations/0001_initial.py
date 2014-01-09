# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Player'
        db.create_table(u'app_player', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('elo_rating', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'app', ['Player'])

        # Adding model 'Tournament'
        db.create_table(u'app_tournament', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('prizes_amount', self.gf('django.db.models.fields.IntegerField')()),
            ('tours_amount', self.gf('django.db.models.fields.IntegerField')(blank=True)),
        ))
        db.send_create_signal(u'app', ['Tournament'])

        # Adding M2M table for field players on 'Tournament'
        m2m_table_name = db.shorten_name(u'app_tournament_players')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tournament', models.ForeignKey(orm[u'app.tournament'], null=False)),
            ('player', models.ForeignKey(orm[u'app.player'], null=False))
        ))
        db.create_unique(m2m_table_name, ['tournament_id', 'player_id'])

        # Adding model 'Tour'
        db.create_table(u'app_tour', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tournament', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Tournament'])),
            ('tour', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'app', ['Tour'])

        # Adding model 'MatchResult'
        db.create_table(u'app_matchresult', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tournament_tour', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Tour'])),
            ('player_one', self.gf('django.db.models.fields.related.ForeignKey')(related_name='Player', to=orm['app.Player'])),
            ('player_one_result', self.gf('django.db.models.fields.FloatField')(default=-1)),
            ('player_two', self.gf('django.db.models.fields.related.ForeignKey')(related_name='Player competitor', to=orm['app.Player'])),
            ('player_two_result', self.gf('django.db.models.fields.FloatField')(default=-1)),
        ))
        db.send_create_signal(u'app', ['MatchResult'])


    def backwards(self, orm):
        # Deleting model 'Player'
        db.delete_table(u'app_player')

        # Deleting model 'Tournament'
        db.delete_table(u'app_tournament')

        # Removing M2M table for field players on 'Tournament'
        db.delete_table(db.shorten_name(u'app_tournament_players'))

        # Deleting model 'Tour'
        db.delete_table(u'app_tour')

        # Deleting model 'MatchResult'
        db.delete_table(u'app_matchresult')


    models = {
        u'app.matchresult': {
            'Meta': {'object_name': 'MatchResult'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player_one': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Player'", 'to': u"orm['app.Player']"}),
            'player_one_result': ('django.db.models.fields.FloatField', [], {'default': '-1'}),
            'player_two': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Player competitor'", 'to': u"orm['app.Player']"}),
            'player_two_result': ('django.db.models.fields.FloatField', [], {'default': '-1'}),
            'tournament_tour': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Tour']"})
        },
        u'app.player': {
            'Meta': {'object_name': 'Player'},
            'elo_rating': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'app.tour': {
            'Meta': {'object_name': 'Tour'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tour': ('django.db.models.fields.IntegerField', [], {}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Tournament']"})
        },
        u'app.tournament': {
            'Meta': {'object_name': 'Tournament'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'players': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['app.Player']", 'symmetrical': 'False'}),
            'prizes_amount': ('django.db.models.fields.IntegerField', [], {}),
            'tours_amount': ('django.db.models.fields.IntegerField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['app']