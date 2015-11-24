# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0013_auto_20151118_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='barangay',
            field=models.CharField(default='CEBU', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='building',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='city',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='province',
            field=models.CharField(default='PROVINCE', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='street',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
