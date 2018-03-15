# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-07 02:01
from __future__ import unicode_literals

import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(help_text='Um nome curto que será usado para identificá-lo de forma única na plataforma', max_length=50, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[\\w.@+-]+$', 32), 'Informe um nome de usuário válido. Este valor deve conter apenas letras e números ', 'invalid')], verbose_name='Usuário')),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='Nome')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='E-mail')),
                ('tel_user', models.CharField(blank=True, max_length=25, null=True, verbose_name='Telefone')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Equipe')),
                ('is_active', models.BooleanField(default=False, verbose_name='Ativo')),
                ('is_masteruser', models.BooleanField(default=True, verbose_name='Usuario Master')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Data de entrada')),
                ('img_user', models.ImageField(blank=True, null=True, upload_to='images', verbose_name='Imagem do perfil')),
                ('qtd_users', models.PositiveIntegerField(blank=True, null=True, verbose_name='Usuarios')),
                ('qtd_unity', models.PositiveIntegerField(blank=True, null=True, verbose_name='Unidades')),
                ('qtd_propriety', models.PositiveIntegerField(blank=True, null=True, verbose_name='Propriedades')),
                ('token', models.CharField(blank=True, max_length=100, verbose_name='Token Senha')),
            ],
            options={
                'verbose_name': 'Usuário',
                'verbose_name_plural': 'Usuários',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
