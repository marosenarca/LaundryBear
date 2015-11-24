# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.contrib.auth.hashers import make_password


def create_superuser(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    user = User(username='admin', password='laundry',
        email='admin@laundrybear.com')
    user.password = make_password(user.password)
    user.is_staff = True
    user.is_superuser = True
    user.save()

class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_auto_20151124_1556'),
    ]

    operations = [
        migrations.RunPython(create_superuser)
    ]
