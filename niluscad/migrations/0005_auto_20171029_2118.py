# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-29 23:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('niluscad', '0004_auto_20171028_0831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='cnpj_cpf',
            field=models.CharField(max_length=20, unique=True, verbose_name='CNPJ/CPF'),
        ),
        migrations.AlterField(
            model_name='company',
            name='razao',
            field=models.CharField(max_length=60, verbose_name='Razão/Nome'),
        ),
    ]
