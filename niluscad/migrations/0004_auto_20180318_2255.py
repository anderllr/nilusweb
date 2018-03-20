# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-19 01:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('niluscad', '0003_auto_20180315_2151'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='c_custo_p',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='niluscad.Ccusto', verbose_name='Plano Financeiro Padrão'),
        ),
        migrations.AddField(
            model_name='company',
            name='plr_finan_p',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='niluscad.PlanoFinan', verbose_name='Plano Financeiro Padrão'),
        ),
    ]
