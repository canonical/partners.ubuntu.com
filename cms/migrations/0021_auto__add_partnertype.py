# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PartnerType'
        db.create_table(u'cms_partnertype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'cms', ['PartnerType'])

        # Adding M2M table for field partner_type on 'Partner'
        m2m_table_name = db.shorten_name(u'cms_partner_partner_type')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('partner', models.ForeignKey(orm[u'cms.partner'], null=False)),
            ('partnertype', models.ForeignKey(orm[u'cms.partnertype'], null=False))
        ))
        db.create_unique(m2m_table_name, ['partner_id', 'partnertype_id'])


    def backwards(self, orm):
        # Deleting model 'PartnerType'
        db.delete_table(u'cms_partnertype')

        # Removing M2M table for field partner_type on 'Partner'
        db.delete_table(db.shorten_name(u'cms_partner_partner_type'))


    models = {
        u'cms.insightstag': {
            'Meta': {'object_name': 'InsightsTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cms.Partner']"}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'cms.link': {
            'Meta': {'object_name': 'Link'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cms.Partner']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'cms.partner': {
            'Meta': {'object_name': 'Partner'},
            'dedicated_partner_page': ('django.db.models.fields.BooleanField', [], {}),
            'fallback_website': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'featured': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'long_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'partner_type': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'partners'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['cms.PartnerType']"}),
            'partner_website': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'programme': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'partners'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['cms.Programme']"}),
            'published': ('django.db.models.fields.BooleanField', [], {}),
            'service_offered': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'partners'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['cms.ServiceOffered']"}),
            'short_description': ('django.db.models.fields.TextField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'technology': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'partners'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['cms.Technology']"})
        },
        u'cms.partnertype': {
            'Meta': {'object_name': 'PartnerType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'cms.programme': {
            'Meta': {'object_name': 'Programme'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'cms.quote': {
            'Meta': {'object_name': 'Quote'},
            'attribution': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cms.Partner']"}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'cms.serviceoffered': {
            'Meta': {'object_name': 'ServiceOffered'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'cms.technology': {
            'Meta': {'object_name': 'Technology'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'cms.text': {
            'Meta': {'object_name': 'Text'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'header': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cms.Partner']"}),
            'read_more_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['cms']