# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-07-13 16:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nilusnfs', '0026_auto_20180606_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notasfiscais',
            name='id_origem',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='ID Externo'),
        ),
    ]
