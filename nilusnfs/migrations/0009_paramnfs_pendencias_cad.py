# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-24 03:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nilusnfs', '0008_auto_20180523_2322'),
    ]

    operations = [
        migrations.AddField(
            model_name='paramnfs',
            name='pendencias_cad',
            field=models.BooleanField(default=False, verbose_name='Pendencias Cadastrais'),
        ),
    ]
