# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-18 01:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usuario', '0002_auto_20170117_1920'),
    ]

    operations = [
        migrations.AddField(
            model_name='grupo',
            name='creador',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
