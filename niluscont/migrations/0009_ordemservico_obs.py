# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-08 01:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('niluscont', '0008_ordemservico'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordemservico',
            name='obs',
            field=models.TextField(blank=True, verbose_name='Observações'),
        ),
    ]
