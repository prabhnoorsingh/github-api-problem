# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-06-24 14:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('githubUsers', '0007_auto_20180624_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetail',
            name='updation_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
