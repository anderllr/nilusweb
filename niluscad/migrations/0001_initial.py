# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-05 01:03
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
            name='Cadgeral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_cad', models.IntegerField(verbose_name='Cod. Cadastro')),
                ('cnpj_cpf', models.CharField(max_length=20, unique=True, verbose_name='CNPJ/CPF')),
                ('razao', models.CharField(max_length=60, verbose_name='Razão/Nome')),
                ('fantasia', models.CharField(blank=True, max_length=40, verbose_name='Fantasia')),
                ('cep', models.CharField(blank=True, max_length=12, null=True, verbose_name='CEP')),
                ('endereco', models.CharField(blank=True, max_length=60, null=True, verbose_name='Endereço')),
                ('numero', models.CharField(blank=True, max_length=10, null=True, verbose_name='Nº')),
                ('complemento', models.CharField(blank=True, max_length=20, null=True, verbose_name='Complemento')),
                ('bairro', models.CharField(blank=True, max_length=40, null=True, verbose_name='Bairro')),
                ('cidade', models.CharField(blank=True, max_length=30, null=True, verbose_name='Cidade')),
                ('uf', models.CharField(blank=True, max_length=2, null=True, verbose_name='UF')),
                ('email', models.EmailField(blank=True, max_length=100, null=True, verbose_name='Email')),
                ('telefone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Telefone')),
                ('data_cadastro', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Data de cadastro')),
                ('situacao', models.BooleanField(default=True, verbose_name='Ativo')),
                ('fornecedor', models.BooleanField(default=False, verbose_name='Fornecedor')),
                ('cliente', models.BooleanField(default=False, verbose_name='Cliente')),
                ('master_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Uusario Master')),
            ],
            options={
                'verbose_name': 'Cadastro',
                'verbose_name_plural': 'Cadastros',
            },
        ),
        migrations.CreateModel(
            name='Ccusto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_ccusto', models.IntegerField(verbose_name='Código')),
                ('descricao', models.CharField(max_length=60, verbose_name='Descricao')),
                ('master_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Uusario Master')),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_company', models.IntegerField(verbose_name='Cod. Empresa')),
                ('cnpj_cpf', models.CharField(max_length=20, unique=True, verbose_name='CNPJ/CPF')),
                ('razao', models.CharField(max_length=60, verbose_name='Razão/Nome')),
                ('fantasia', models.CharField(blank=True, max_length=40, verbose_name='Fantasia')),
                ('cep', models.CharField(blank=True, max_length=12, null=True, verbose_name='CEP')),
                ('endereco', models.CharField(blank=True, max_length=60, null=True, verbose_name='Endereço')),
                ('numero', models.CharField(blank=True, max_length=10, null=True, verbose_name='Nº')),
                ('complemento', models.CharField(blank=True, max_length=20, null=True, verbose_name='Complemento')),
                ('bairro', models.CharField(blank=True, max_length=40, null=True, verbose_name='Bairro')),
                ('cidade', models.CharField(blank=True, max_length=30, null=True, verbose_name='Cidade')),
                ('uf', models.CharField(blank=True, max_length=2, null=True, verbose_name='UF')),
                ('email', models.EmailField(blank=True, max_length=100, null=True, verbose_name='Email')),
                ('telefone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Telefone')),
                ('data_cadastro', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Data de cadastro')),
                ('situacao', models.BooleanField(default=True, verbose_name='Ativo')),
                ('master_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Uusario Master')),
            ],
            options={
                'verbose_name': 'Empresa',
                'verbose_name_plural': 'Empresas',
            },
        ),
        migrations.CreateModel(
            name='PlanoFinan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_plfin', models.IntegerField(verbose_name='Código')),
                ('descricao', models.CharField(max_length=60, verbose_name='Descricao')),
                ('sinal', models.CharField(choices=[('D', 'Despesas'), ('R', 'Receitas')], max_length=1, verbose_name='Sinal Conta')),
                ('master_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Uusario Master')),
            ],
        ),
        migrations.CreateModel(
            name='Propriety',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_propriety', models.IntegerField(verbose_name='Cod. Propriedade')),
                ('ie', models.CharField(max_length=20, unique=True, verbose_name='I.E*')),
                ('razao', models.CharField(max_length=60, verbose_name='Razão/Nome*')),
                ('fantasia', models.CharField(blank=True, max_length=40, verbose_name='Fantasia')),
                ('cep', models.CharField(blank=True, max_length=12, null=True, verbose_name='CEP')),
                ('endereco', models.CharField(blank=True, max_length=60, null=True, verbose_name='Endereço')),
                ('numero', models.CharField(blank=True, max_length=10, null=True, verbose_name='Nº')),
                ('complemento', models.CharField(blank=True, max_length=20, null=True, verbose_name='Complemento')),
                ('bairro', models.CharField(blank=True, max_length=40, null=True, verbose_name='Bairro')),
                ('cidade', models.CharField(blank=True, max_length=30, null=True, verbose_name='Cidade')),
                ('uf', models.CharField(blank=True, max_length=2, null=True, verbose_name='UF')),
                ('email', models.EmailField(blank=True, max_length=100, null=True, verbose_name='Email')),
                ('telefone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Telefone')),
                ('data_cadastro', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Data de cadastro')),
                ('situacao', models.BooleanField(default=True, verbose_name='Ativo')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='niluscad.Company', verbose_name='Empresa Vinculada')),
                ('master_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Uusario Master')),
            ],
            options={
                'verbose_name': 'Propriedade',
                'verbose_name_plural': 'Propriedades',
            },
        ),
        migrations.AlterUniqueTogether(
            name='propriety',
            unique_together=set([('master_user', 'num_propriety'), ('master_user', 'ie'), ('master_user', 'num_propriety', 'company')]),
        ),
        migrations.AlterUniqueTogether(
            name='company',
            unique_together=set([('master_user', 'num_company'), ('master_user', 'cnpj_cpf')]),
        ),
        migrations.AlterUniqueTogether(
            name='cadgeral',
            unique_together=set([('master_user', 'num_cad'), ('master_user', 'cnpj_cpf')]),
        ),
    ]
