# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-02 02:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('niluscad', '0006_auto_20180423_2210'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nilusnfs', '0004_auto_20180501_2321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paramnfs',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='niluscad.Company', verbose_name='Empresa'),
        ),
        migrations.AlterUniqueTogether(
            name='paramnfs',
            unique_together=set([('master_user', 'company')]),
        ),
    ]