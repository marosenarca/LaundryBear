# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LaundryShop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('province', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50, blank=True)),
                ('barangay', models.CharField(max_length=50)),
                ('street', models.CharField(max_length=50, blank=True)),
                ('building', models.CharField(max_length=50, blank=True)),
                ('contact_number', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254, blank=True)),
                ('website', models.URLField(blank=True)),
                ('hours_open', models.CharField(max_length=100)),
                ('days_open', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('laundry_shop', models.ForeignKey(to='database.LaundryShop')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('paws', models.IntegerField(null=True, blank=True)),
                ('laundry_shop', models.ForeignKey(related_name='ratings', to='database.LaundryShop')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('prices', models.ManyToManyField(related_name='services', through='database.Price', to='database.LaundryShop')),
            ],
        ),
        migrations.AddField(
            model_name='price',
            name='service',
            field=models.ForeignKey(to='database.Service'),
        ),
    ]
