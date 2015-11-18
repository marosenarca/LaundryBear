# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import database.models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0012_price_duration'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pieces', models.IntegerField(default=0)),
                ('price', models.ForeignKey(to='database.Price')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(default=1, choices=[(1, b'Pending'), (2, b'Ongoing'), (3, b'Done'), (4, b'Rejected')])),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('delivery_date', models.DateField(default=database.models.default_date)),
                ('client', models.ForeignKey(to='database.UserProfile')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='transaction',
            field=models.ForeignKey(to='database.Transaction'),
        ),
    ]
