# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_fees(apps, schema_editor):
    Fees = apps.get_model('database', 'Fees')
    Site = apps.get_model('sites', 'Site')
    Fees.objects.create(site=Site.objects.get_current())


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_create_admin_user'),
    ]

    operations = [
        migrations.RunPython(create_fees),
    ]
