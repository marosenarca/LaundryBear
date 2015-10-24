# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_laundryshop_creation_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='laundryshop',
            options={'get_latest_by': 'creation_date'},
        ),
    ]
