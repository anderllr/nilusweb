# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-05 02:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0003_auto_20171105_0049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instancia',
            name='company',
            field=models.IntegerField(null=True, verbose_name='Empresa padrão PK'),
        ),
        migrations.AlterField(
            model_name='instancia',
            name='propriety',
            field=models.IntegerField(null=True, verbose_name='Propriedade Padrão PK'),
        ),
    ]
