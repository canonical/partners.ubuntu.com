# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'cms_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'cms', ['Category'])

        # Adding model 'IndustrySector'
        db.create_table(u'cms_industrysector', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'cms', ['IndustrySector'])

        # Adding model 'Programme'
        db.create_table(u'cms_programme', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'cms', ['Programme'])

        # Adding model 'ServiceOffered'
        db.create_table(u'cms_serviceoffered', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'cms', ['ServiceOffered'])

        # Adding model 'Region'
        db.create_table(u'cms_region', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'cms', ['Region'])

        # Adding model 'Partner'
        db.create_table(u'cms_partner', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.CharField')(default='TEST_USER', max_length=200, blank=True)),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('updated_by', self.gf('django.db.models.fields.CharField')(default='TEST_USER', max_length=200, blank=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')()),
            ('logo', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('external_page', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('external_fallback', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('short_description', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('long_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('featured', self.gf('django.db.models.fields.BooleanField')()),
            ('generate_page', self.gf('django.db.models.fields.BooleanField')()),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'cms', ['Partner'])

        # Adding M2M table for field category on 'Partner'
        m2m_table_name = db.shorten_name(u'cms_partner_category')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('partner', models.ForeignKey(orm[u'cms.partner'], null=False)),
            ('category', models.ForeignKey(orm[u'cms.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['partner_id', 'category_id'])

        # Adding M2M table for field industry_sector on 'Partner'
        m2m_table_name = db.shorten_name(u'cms_partner_industry_sector')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('partner', models.ForeignKey(orm[u'cms.partner'], null=False)),
            ('industrysector', models.ForeignKey(orm[u'cms.industrysector'], null=False))
        ))
        db.create_unique(m2m_table_name, ['partner_id', 'industrysector_id'])

        # Adding M2M table for field programme on 'Partner'
        m2m_table_name = db.shorten_name(u'cms_partner_programme')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('partner', models.ForeignKey(orm[u'cms.partner'], null=False)),
            ('programme', models.ForeignKey(orm[u'cms.programme'], null=False))
        ))
        db.create_unique(m2m_table_name, ['partner_id', 'programme_id'])

        # Adding M2M table for field service_offered on 'Partner'
        m2m_table_name = db.shorten_name(u'cms_partner_service_offered')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('partner', models.ForeignKey(orm[u'cms.partner'], null=False)),
            ('serviceoffered', models.ForeignKey(orm[u'cms.serviceoffered'], null=False))
        ))
        db.create_unique(m2m_table_name, ['partner_id', 'serviceoffered_id'])

        # Adding M2M table for field region on 'Partner'
        m2m_table_name = db.shorten_name(u'cms_partner_region')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('partner', models.ForeignKey(orm[u'cms.partner'], null=False)),
            ('region', models.ForeignKey(orm[u'cms.region'], null=False))
        ))
        db.create_unique(m2m_table_name, ['partner_id', 'region_id'])

        # Adding model 'Quote'
        db.create_table(u'cms_quote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('partner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Partner'])),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('attribution', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'cms', ['Quote'])

        # Adding model 'Link'
        db.create_table(u'cms_link', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('partner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Partner'])),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'cms', ['Link'])

        # Adding model 'InsightsTag'
        db.create_table(u'cms_insightstag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('partner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Partner'])),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'cms', ['InsightsTag'])

        # Adding model 'Text'
        db.create_table(u'cms_text', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('partner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Partner'])),
            ('image', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('header', self.gf('django.db.models.fields.TextField')()),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'cms', ['Text'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'cms_category')

        # Deleting model 'IndustrySector'
        db.delete_table(u'cms_industrysector')

        # Deleting model 'Programme'
        db.delete_table(u'cms_programme')

        # Deleting model 'ServiceOffered'
        db.delete_table(u'cms_serviceoffered')

        # Deleting model 'Region'
        db.delete_table(u'cms_region')

        # Deleting model 'Partner'
        db.delete_table(u'cms_partner')

        # Removing M2M table for field category on 'Partner'
        db.delete_table(db.shorten_name(u'cms_partner_category'))

        # Removing M2M table for field industry_sector on 'Partner'
        db.delete_table(db.shorten_name(u'cms_partner_industry_sector'))

        # Removing M2M table for field programme on 'Partner'
        db.delete_table(db.shorten_name(u'cms_partner_programme'))

        # Removing M2M table for field service_offered on 'Partner'
        db.delete_table(db.shorten_name(u'cms_partner_service_offered'))

        # Removing M2M table for field region on 'Partner'
        db.delete_table(db.shorten_name(u'cms_partner_region'))

        # Deleting model 'Quote'
        db.delete_table(u'cms_quote')

        # Deleting model 'Link'
        db.delete_table(u'cms_link')

        # Deleting model 'InsightsTag'
        db.delete_table(u'cms_insightstag')

        # Deleting model 'Text'
        db.delete_table(u'cms_text')


    models = {
        u'cms.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'cms.industrysector': {
            'Meta': {'object_name': 'IndustrySector'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
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
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'partners'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['cms.Category']"}),
            'created_by': ('django.db.models.fields.CharField', [], {'default': "'TEST_USER'", 'max_length': '200', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'external_fallback': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'external_page': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {}),
            'generate_page': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry_sector': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'partners'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['cms.IndustrySector']"}),
            'logo': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'programme': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'partners'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['cms.Programme']"}),
            'published': ('django.db.models.fields.BooleanField', [], {}),
            'region': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'partners'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['cms.Region']"}),
            'service_offered': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'partners'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['cms.ServiceOffered']"}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.CharField', [], {'default': "'TEST_USER'", 'max_length': '200', 'blank': 'True'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
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
        u'cms.region': {
            'Meta': {'object_name': 'Region'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'cms.serviceoffered': {
            'Meta': {'object_name': 'ServiceOffered'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'cms.text': {
            'Meta': {'object_name': 'Text'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'header': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cms.Partner']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['cms']