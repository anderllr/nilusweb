# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-09 00:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_user_qtd_propriety'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='conta_presente',
            field=models.BooleanField(default=False, verbose_name='Conta Presente'),
        ),
    ]