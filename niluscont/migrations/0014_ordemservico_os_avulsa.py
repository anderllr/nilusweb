# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-06-03 20:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('niluscont', '0013_auto_20180516_2317'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordemservico',
            name='os_avulsa',
            field=models.BooleanField(default=False, verbose_name='OS Avulsa'),
        ),
    ]
