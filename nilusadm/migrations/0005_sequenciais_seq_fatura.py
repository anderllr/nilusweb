# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-07-13 15:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nilusadm', '0004_sequenciais_ordensservico'),
    ]

    operations = [
        migrations.AddField(
            model_name='sequenciais',
            name='seq_fatura',
            field=models.IntegerField(default=0, verbose_name='Seq Faturamento'),
        ),
    ]