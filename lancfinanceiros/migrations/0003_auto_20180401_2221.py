# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-02 01:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lancfinanceiros', '0002_auto_20180327_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lancamentos',
            name='cadgeral',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='niluscad.Cadgeral', verbose_name='Cliente'),
        ),
        migrations.AlterField(
            model_name='lancamentos',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='niluscad.Company', verbose_name='Empresa'),
        ),
        migrations.AlterField(
            model_name='lancamentos',
            name='conta_finan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='nilusfin.Contafinanceira', verbose_name='Conta Recebimento'),
        ),
        migrations.AlterField(
            model_name='lancamentos',
            name='plr_financeiro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='niluscad.PlanoFinan', verbose_name='Plano Financeiro'),
        ),
        migrations.AlterField(
            model_name='movtos_lancamentos',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='niluscad.Company', verbose_name='empresa'),
        ),
        migrations.AlterField(
            model_name='movtos_lancamentos',
            name='conta_financeira',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='nilusfin.Contafinanceira', verbose_name='Conta Financeira'),
        ),
    ]
