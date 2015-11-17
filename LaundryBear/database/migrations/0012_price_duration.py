# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0011_auto_20151104_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='duration',
            field=models.IntegerField(default=3),
            preserve_default=False,
        ),
    ]
