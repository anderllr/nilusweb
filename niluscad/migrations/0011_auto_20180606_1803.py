# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-06-06 21:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('niluscad', '0010_auto_20180606_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cadgeral',
            name='complemento',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='Complemento'),
        ),
        migrations.AlterField(
            model_name='propriety',
            name='complemento',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='Complemento'),
        ),
    ]
