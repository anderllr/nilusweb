# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-14 16:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lancfinanceiros', '0009_lancamentos_saldo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lancamentos',
            old_name='saldo',
            new_name='valor_original',
        ),
    ]
