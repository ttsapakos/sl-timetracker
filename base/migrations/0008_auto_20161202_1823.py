# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-02 23:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_enrollment_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='meeting_days',
            field=models.CharField(default='MWR', max_length=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='enrollment',
            name='meeting_end_time',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='enrollment',
            name='meeting_start_time',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
