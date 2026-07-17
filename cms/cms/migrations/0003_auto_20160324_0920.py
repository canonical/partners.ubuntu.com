# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("cms", "0002_auto_20160309_1631")]

    operations = [
        migrations.AddField(
            model_name="text",
            name="insights_tag",
            field=models.CharField(
                help_text=(
                    b"Articles matching this insigts tag will be"
                    b" included in the block. Leave blank for no"
                    b" insights feed."
                ),
                max_length=200,
                blank=True,
            ),
        ),
        migrations.AddField(
            model_name="text",
            name="read_more_cta",
            field=models.BooleanField(
                default=False,
                help_text=b"Should the 'read more' link be a CTA button?",
            ),
        ),
        migrations.AddField(
            model_name="text",
            name="read_more_link_text",
            field=models.CharField(
                help_text=(
                    b"The content of the field's link. Leave blank for"
                    b" 'read more'"
                ),
                max_length=200,
                blank=True,
            ),
        ),
        migrations.AddField(
            model_name="text",
            name="video_url",
            field=models.URLField(
                help_text=(
                    b"A Youtube video URL. Note: This will override any"
                    b" image for this text block."
                ),
                null=True,
                blank=True,
            ),
        ),
    ]
