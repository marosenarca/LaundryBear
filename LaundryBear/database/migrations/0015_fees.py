# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0014_auto_20151123_2003'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fees',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('delivery_fee', models.DecimalField(default=50, max_digits=4, decimal_places=2)),
                ('service_charge', models.DecimalField(default=0.1, max_digits=3, decimal_places=2)),
            ],
        ),
    ]
