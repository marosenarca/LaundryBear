# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('database', '0015_fees'),
    ]

    operations = [
        migrations.AddField(
            model_name='fees',
            name='site',
            field=models.OneToOneField(default=1, to='sites.Site'),
            preserve_default=False,
        ),
    ]
