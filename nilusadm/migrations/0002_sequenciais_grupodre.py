# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-16 00:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nilusadm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sequenciais',
            name='grupodre',
            field=models.IntegerField(default=0, verbose_name='Seq Lancamento Financeiro'),
        ),
    ]
