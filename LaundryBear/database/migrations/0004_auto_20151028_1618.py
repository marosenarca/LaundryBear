# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_auto_20151024_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='paws',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
