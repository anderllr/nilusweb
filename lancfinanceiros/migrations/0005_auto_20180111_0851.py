# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-11 10:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lancfinanceiros', '0004_lancamentos_descricao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lancamentos',
            name='descricao',
            field=models.CharField(max_length=20, null=True, verbose_name='Observação'),
        ),
    ]
