# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Tournament.tours_amount'
        db.alter_column(u'app_tournament', 'tours_amount', self.gf('django.db.models.fields.IntegerField')(null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Tournament.tours_amount'
        raise RuntimeError("Cannot reverse this migration. 'Tournament.tours_amount' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Tournament.tours_amount'
        db.alter_column(u'app_tournament', 'tours_amount', self.gf('django.db.models.fields.IntegerField')())

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
            'tours_amount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['app']