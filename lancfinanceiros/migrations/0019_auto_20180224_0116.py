# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-24 04:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lancfinanceiros', '0018_auto_20180224_0113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movtos_lancamentos',
            name='tipo_movto',
            field=models.CharField(choices=[('C', 'Criação'), ('B', 'Baixa'), ('D', 'Desconto'), ('J', 'Juros'), ('M', 'Multa'), ('A', 'Ajuste Saldo')], max_length=1, verbose_name='Tipo'),
        ),
    ]
