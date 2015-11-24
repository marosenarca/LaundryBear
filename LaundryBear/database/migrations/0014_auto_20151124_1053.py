# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0013_auto_20151118_1924'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='laundry_shop',
        ),
        migrations.AddField(
            model_name='transaction',
            name='paws',
            field=models.IntegerField(default=4),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
    ]
