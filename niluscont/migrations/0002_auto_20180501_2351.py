# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-02 02:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('niluscont', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contratos',
            name='valor',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=13, null=True, verbose_name='Valor'),
        ),
        migrations.AddField(
            model_name='contratos',
            name='valor_text',
            field=models.CharField(default=1, max_length=20, verbose_name='Valor'),
            preserve_default=False,
        ),
    ]
