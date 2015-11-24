# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_create_fees_entry'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
