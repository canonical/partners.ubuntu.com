# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0002_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='tags_label',
            field=models.TextField(help_text=b'The displayed name for the tags list', blank=True),
        ),
    ]
