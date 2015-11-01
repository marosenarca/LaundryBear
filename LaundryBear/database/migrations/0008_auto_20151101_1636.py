# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0007_auto_20151101_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='client',
            field=models.ForeignKey(related_name='profile', blank=True, to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
