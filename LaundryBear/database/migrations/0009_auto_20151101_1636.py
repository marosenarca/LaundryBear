# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0008_auto_20151101_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='client',
            field=models.OneToOneField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
