# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-06-06 21:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('niluscad', '0009_auto_20180606_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propriety',
            name='complemento',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='Complemento'),
        ),
    ]