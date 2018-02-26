# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-24 04:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recebiveis', '0009_auto_20171204_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recebiveis',
            name='c_custo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='niluscad.Ccusto', verbose_name='Centro de Custo'),
        ),
        migrations.AlterField(
            model_name='recebiveis',
            name='conta_receb',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='nilusfin.Contafinanceira', verbose_name='Conta Recebimento'),
        ),
        migrations.AlterField(
            model_name='recebiveis',
            name='cotacao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='nilusfin.Cotacao'),
        ),
        migrations.AlterField(
            model_name='recebiveis',
            name='indice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='nilusfin.Indice'),
        ),
        migrations.AlterField(
            model_name='recebiveis',
            name='plr_financeiro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='niluscad.PlanoFinan', verbose_name='Plano Financeiro'),
        ),
    ]
