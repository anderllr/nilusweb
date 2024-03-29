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
            options={
                'verbose_name': 'C. Custo',
                'verbose_name_plural': 'C. Custos',
            },
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
                ('master_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usario Master')),
            ],
            options={
                'verbose_name': 'Empresa',
                'verbose_name_plural': 'Empresas',
            },
        ),
        migrations.CreateModel(
            name='Grupodre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_grupodre', models.IntegerField(verbose_name='Código')),
                ('descricao', models.CharField(max_length=20, verbose_name='Nome Grupo')),
                ('ordem', models.PositiveIntegerField(verbose_name='Ordem no relatório')),
                ('sinal', models.CharField(choices=[(None, 'Informe o calculo'), ('+', 'Soma'), ('-', 'Subtrai')], max_length=1, verbose_name='Sinal Conta')),
                ('master_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario Master')),
            ],
            options={
                'verbose_name': 'Grupo DRE',
                'verbose_name_plural': 'Grupos DRE',
            },
        ),
        migrations.CreateModel(
            name='PlanoFinan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_plfin', models.IntegerField(verbose_name='Código')),
                ('descricao', models.CharField(max_length=60, verbose_name='Descricão')),
                ('sinal', models.CharField(choices=[(None, 'Informe o sinal'), ('D', 'Despesas'), ('R', 'Receitas')], max_length=1, verbose_name='Sinal Conta')),
                ('grupodre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='plano_financeiro', to='niluscad.Grupodre', verbose_name='Grupo Dre')),
                ('master_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario Master')),
            ],
            options={
                'verbose_name': 'Plano Financeiro',
                'verbose_name_plural': 'Plano Financeiro',
            },
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
                ('area', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Área M²')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='niluscad.Company', verbose_name='Empresa Vinculada')),
                ('master_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Uusario Master')),
            ],
            options={
                'verbose_name': 'Propriedade',
                'verbose_name_plural': 'Propriedades',
            },
        ),
        migrations.CreateModel(
            name='Talhao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.DecimalField(blank=True, decimal_places=2, max_digits=13, null=True, verbose_name='Área')),
                ('talhao', models.CharField(max_length=50, verbose_name='Nome Talhão')),
                ('propriety', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='niluscad.Propriety', verbose_name='Propriedade')),
                ('user_cad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario Criação')),
            ],
            options={
                'verbose_name': 'Talhão',
                'verbose_name_plural': 'Talhões',
            },
        ),
        migrations.AlterUniqueTogether(
            name='propriety',
            unique_together=set([('master_user', 'num_propriety'), ('master_user', 'ie'), ('master_user', 'num_propriety', 'company')]),
        ),
        migrations.AlterUniqueTogether(
            name='planofinan',
            unique_together=set([('master_user', 'num_plfin')]),
        ),
        migrations.AlterUniqueTogether(
            name='grupodre',
            unique_together=set([('master_user', 'num_grupodre')]),
        ),
        migrations.AlterUniqueTogether(
            name='ccusto',
            unique_together=set([('master_user', 'num_ccusto')]),
        ),
        migrations.AlterUniqueTogether(
            name='cadgeral',
            unique_together=set([('master_user', 'num_cad'), ('master_user', 'cnpj_cpf')]),
        ),
    ]
