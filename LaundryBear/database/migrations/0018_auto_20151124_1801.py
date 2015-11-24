# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0017_auto_20151124_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='paws',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
