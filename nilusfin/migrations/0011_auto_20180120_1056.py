# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-20 12:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nilusfin', '0010_auto_20180116_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cotacao',
            name='user_cad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario Criação'),
        ),
    ]
