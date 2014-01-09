# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Tournament.is_finished'
        db.add_column(u'app_tournament', 'is_finished',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Tournament.is_finished'
        db.delete_column(u'app_tournament', 'is_finished')


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
            'is_finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'players': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['app.Player']", 'symmetrical': 'False'}),
            'prizes_amount': ('django.db.models.fields.IntegerField', [], {}),
            'tours_amount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['app']