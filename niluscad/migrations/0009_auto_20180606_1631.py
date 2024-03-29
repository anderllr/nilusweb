# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-06-06 19:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('niluscad', '0008_auto_20180526_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cadgeral',
            name='cnpj_cpf',
            field=models.CharField(max_length=20, verbose_name='CNPJ/CPF'),
        ),
        migrations.AlterField(
            model_name='company',
            name='cnpj_cpf',
            field=models.CharField(max_length=20, verbose_name='CNPJ/CPF'),
        ),
        migrations.AlterField(
            model_name='propriety',
            name='ie',
            field=models.CharField(max_length=20, verbose_name='I.E*'),
        ),
        migrations.AlterUniqueTogether(
            name='company',
            unique_together=set([('master_user', 'cnpj_cpf'), ('master_user', 'num_company')]),
        ),
    ]
