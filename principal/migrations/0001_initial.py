# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-16 00:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('niluscad', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Instancia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='niluscad.Company', verbose_name='Empresa padrão')),
                ('propriety', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='niluscad.Propriety', verbose_name='Propriedade Padrão')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Instancia',
                'verbose_name_plural': 'Instancias',
            },
        ),
    ]
