# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.hashers import make_password
from django.db import migrations, models


def create_superuser(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    UserProfile = apps.get_model('database', 'UserProfile')
    user = User(username='admin', password='laundry',
        email='admin@laundrybear.com')
    user.password = make_password(user.password)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    profile = UserProfile(client=user, contact_number='00000000000',
        province='Cebu', city='Cebu City', barangay='Lahug',
        street='Gorordo Avenue', building='A.S. Building')
    profile.save()


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_superuser)
    ]
