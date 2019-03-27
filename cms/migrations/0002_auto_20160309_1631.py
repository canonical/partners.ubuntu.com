# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("cms", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("tag", models.CharField(help_text=b"", max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name="partner",
            name="tags_label",
            field=models.CharField(
                help_text=b"The displayed name for the tags list",
                max_length=200,
                blank=True,
            ),
        ),
        migrations.AddField(
            model_name="tag",
            name="partner",
            field=models.ForeignKey(to="cms.Partner"),
        ),
    ]
