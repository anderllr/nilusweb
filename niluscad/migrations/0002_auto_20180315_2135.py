# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-16 00:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('niluscad', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='endereco',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Endereço'),
        ),
    ]
