# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-18 05:25
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='author',
            managers=[
                ('authorManager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='book',
            managers=[
                ('bookManager', django.db.models.manager.Manager()),
            ],
        ),
    ]