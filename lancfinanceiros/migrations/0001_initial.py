# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-16 00:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('nilusfin', '0001_initial'),
        ('niluscad', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lancamentos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_lan', models.IntegerField(verbose_name='Nº Registro')),
                ('parcela', models.IntegerField(default=1, verbose_name='Parcela')),
                ('dt_lancamento', models.DateField(blank=True, null=True, verbose_name='Data Lançamento')),
                ('dt_vencimento', models.DateField(blank=True, null=True, verbose_name='Data Vencimento')),
                ('vlr_lancamento', models.DecimalField(blank=True, decimal_places=2, max_digits=13, null=True, verbose_name='Valor do Lançamento')),
                ('valor_text', models.CharField(max_length=20, verbose_name='Valor')),
                ('saldo', models.DecimalField(blank=True, decimal_places=2, max_digits=13, null=True, verbose_name='Saldo')),
                ('descricao', models.CharField(blank=True, max_length=70, null=True, verbose_name='Observação')),
                ('titulo', models.BooleanField(default=False, verbose_name='É Titulo')),
                ('situacao', models.BooleanField(default=False, verbose_name='Baixado')),
                ('reaberto', models.BooleanField(default=False, verbose_name='Reaberto')),
                ('data_baixa', models.DateField(blank=True, null=True, verbose_name='Data de Recebimento')),
                ('tipo_lancamento', models.CharField(choices=[('R', 'Receita'), ('D', 'Despesa')], max_length=1, verbose_name='Tipo')),
                ('c_custo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='niluscad.Ccusto', verbose_name='Centro de Custo')),
                ('cadgeral', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='niluscad.Cadgeral', verbose_name='Cliente')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='niluscad.Company', verbose_name='Empresa')),
                ('conta_finan', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='nilusfin.Contafinanceira', verbose_name='Conta Recebimento')),
                ('cotacao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='nilusfin.Cotacao')),
                ('indice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='nilusfin.Indice')),
                ('lancamento_pai', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lancfinanceiros.Lancamentos', verbose_name='Lançamento Pai')),
                ('master_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario Master')),
                ('plr_financeiro', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='niluscad.PlanoFinan', verbose_name='Plano Financeiro')),
            ],
            options={
                'verbose_name': 'Lançamento',
                'verbose_name_plural': 'Lançamentos',
            },
        ),
        migrations.CreateModel(
            name='Movtos_lancamentos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt_movimento', models.DateField(verbose_name='Data Movimento')),
                ('vlr_movimento', models.DecimalField(blank=True, decimal_places=2, max_digits=13, null=True, verbose_name='Valor do Lançamento')),
                ('desc_movimento', models.CharField(max_length=70, null=True, verbose_name='Observação')),
                ('sinal', models.CharField(max_length=3, verbose_name='Sinal da Conta')),
                ('tipo_movto', models.CharField(choices=[('C', 'Criação'), ('B', 'Baixa'), ('D', 'Desconto'), ('J', 'Juros'), ('M', 'Multa'), ('A', 'Ajuste Saldo')], max_length=1, verbose_name='Tipo')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='niluscad.Company', verbose_name='empresa')),
                ('conta_financeira', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='nilusfin.Contafinanceira', verbose_name='Conta Financeira')),
                ('lancamento', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='lancfinanceiros.Lancamentos', verbose_name='lancamento')),
                ('master_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario Master')),
            ],
            options={
                'verbose_name': 'Movimentos',
                'verbose_name_plural': 'Movimentos',
            },
        ),
        migrations.AlterUniqueTogether(
            name='lancamentos',
            unique_together=set([('master_user', 'num_lan', 'parcela')]),
        ),
    ]
