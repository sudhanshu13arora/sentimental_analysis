# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-24 04:41
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reviews', '0005_auto_20180424_0515'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Plots',
        ),
        migrations.AddField(
            model_name='reviews',
            name='score',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='timetables',
            name='date_t',
            field=models.DateField(default=datetime.date.today, unique_for_date=True),
        ),
    ]
