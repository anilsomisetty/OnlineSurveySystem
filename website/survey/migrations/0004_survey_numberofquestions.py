# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-03 19:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0003_auto_20180402_2208'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='numberofquestions',
            field=models.IntegerField(default=0),
        ),
    ]