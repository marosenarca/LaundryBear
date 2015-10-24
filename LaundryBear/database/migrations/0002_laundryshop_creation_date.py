# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='laundryshop',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 24, 15, 31, 20, 789198, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
