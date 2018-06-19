# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-16 00:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Permissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nilusCadastro', models.BooleanField(default=False, verbose_name='Cadastros')),
                ('nilusFinanceiro', models.BooleanField(default=False, verbose_name='Financeiro')),
                ('nilusCompras', models.BooleanField(default=False, verbose_name='Compras')),
                ('nilusProducao', models.BooleanField(default=False, verbose_name='Producao')),
                ('nilusMaquinas', models.BooleanField(default=False, verbose_name='Máquinas')),
                ('nilusFiscalCont', models.BooleanField(default=False, verbose_name='Fiscal e Contábil')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
        ),
        migrations.CreateModel(
            name='Sequenciais',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empresas', models.IntegerField(default=0, verbose_name='Seq Cad. Empresas')),
                ('propriedades', models.IntegerField(default=0, verbose_name='Seq Cad. Propriedades')),
                ('cadgeral', models.IntegerField(default=0, verbose_name='Seq Cad. CadGeral')),
                ('ccusto', models.IntegerField(default=0, verbose_name='Seq Cad. Ccusto')),
                ('planofinan', models.IntegerField(default=0, verbose_name='Seq PlanoFinan')),
                ('conta', models.IntegerField(default=0, verbose_name='Seq Conta')),
                ('indice', models.IntegerField(default=0, verbose_name='Seq Indice')),
                ('recebiveis', models.IntegerField(default=0, verbose_name='Seq Tit. Receber')),
                ('lanc_financeiros', models.IntegerField(default=0, verbose_name='Seq Lancamento Financeiro')),
                ('grupodre', models.IntegerField(default=0, verbose_name='Seq Lancamento Financeiro')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
        ),
    ]