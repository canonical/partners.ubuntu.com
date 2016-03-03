# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
from django.contrib.auth.models import Group


def create_groups(apps, schema_editor):
    authors = Group(name='partners.u.c-authors')
    authors.save()

class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InsightsTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(help_text=b'Link to a tag on insights.ubuntu.com and pulls in the RSS feed to the partner page.', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('slug', models.SlugField(help_text=b'Auto-generated, for use in URLs', unique=True)),
                ('published', models.BooleanField(help_text=b'Partners without this checked will never be seen by the public')),
                ('logo', models.URLField(help_text=b'The URL to the logo (e.g. http://example.com/logo.svg).\nPlease only upload .png and .svg files, no less than 200 pixels wide.\n')),
                ('partner_website', models.URLField(help_text=b"The URL to the partner's site where the info about partnering with Canonical is.")),
                ('fallback_website', models.URLField(help_text=b"If our partner changes their site without us realising it, and the 'external page' errors, this will be` used instead.")),
                ('short_description', models.TextField(help_text=b"Used in search results, max 375 characters.(<a href='http://daringfireball.net/projects/markdown/basics'>Markdown formatted</a>)", validators=[django.core.validators.MaxLengthValidator(375)])),
                ('long_description', models.TextField(help_text=b"Only displayed on the dedicated partner page (when 'generate page' is selected). (<a href='http://daringfireball.net/projects/markdown/basics'>Markdown formatted</a>)", null=True, blank=True)),
                ('featured', models.BooleanField(help_text=b'Promote to the front page')),
                ('always_featured', models.BooleanField(default=False, help_text=b'Always promote to the top of lists.')),
                ('dedicated_partner_page', models.BooleanField(help_text=b"Does this partner have it's own dedicated page?")),
                ('notes', models.TextField(help_text=b'Private, for internal Canonical use', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PartnerType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'partner type',
            },
        ),
        migrations.CreateModel(
            name='Programme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'programme',
            },
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(blank=True)),
                ('attribution', models.CharField(max_length=200)),
                ('partner', models.ForeignKey(to='cms.Partner')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceOffered',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'service offered',
            },
        ),
        migrations.CreateModel(
            name='Technology',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'technology',
            },
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image_url', models.URLField(help_text=b'A URL for an image to appear alongside the text')),
                ('header', models.TextField()),
                ('body', models.TextField()),
                ('read_more_link', models.URLField(null=True, blank=True)),
                ('partner', models.ForeignKey(to='cms.Partner')),
            ],
        ),
        migrations.AddField(
            model_name='partner',
            name='partner_type',
            field=models.ManyToManyField(help_text=b'test', related_name='partners', null=True, to='cms.PartnerType', blank=True),
        ),
        migrations.AddField(
            model_name='partner',
            name='programme',
            field=models.ManyToManyField(related_name='partners', null=True, to='cms.Programme', blank=True),
        ),
        migrations.AddField(
            model_name='partner',
            name='service_offered',
            field=models.ManyToManyField(related_name='partners', null=True, to='cms.ServiceOffered', blank=True),
        ),
        migrations.AddField(
            model_name='partner',
            name='technology',
            field=models.ManyToManyField(related_name='partners', null=True, to='cms.Technology', blank=True),
        ),
        migrations.AddField(
            model_name='link',
            name='partner',
            field=models.ForeignKey(to='cms.Partner'),
        ),
        migrations.AddField(
            model_name='insightstag',
            name='partner',
            field=models.ForeignKey(to='cms.Partner'),
        ),
        migrations.RunPython(create_groups),
    ]
