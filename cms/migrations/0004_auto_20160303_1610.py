# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_partner_tags_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='tags_label',
            field=models.CharField(help_text=b'The displayed name for the tags list', max_length=200, blank=True),
        ),
    ]
