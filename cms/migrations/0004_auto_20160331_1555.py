# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_auto_20160324_0920'),
    ]

    operations = [
        migrations.AddField(
            model_name='text',
            name='html_class',
            field=models.CharField(help_text=b'The class added to the generated HTML for this section', max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='text',
            name='read_more_external',
            field=models.BooleanField(default=False, help_text=b"Does the 'read more' link to an external site (other canonical sites or subdomains count as external)?"),
        ),
        migrations.AlterField(
            model_name='text',
            name='image_url',
            field=models.URLField(help_text=b'A URL for an image to appear alongside the text', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='text',
            name='video_url',
            field=models.URLField(help_text=b'A Youtube video URL.', null=True, blank=True),
        ),
    ]
