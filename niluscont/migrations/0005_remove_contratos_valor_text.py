# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-05 01:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('niluscont', '0004_auto_20180502_2339'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contratos',
            name='valor_text',
        ),
    ]
