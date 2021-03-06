# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-26 10:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Excelinp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('ID', models.SmallIntegerField(primary_key=True, serialize=False)),
                ('Code', models.CharField(max_length=20, unique=True)),
                ('Description', models.CharField(max_length=200)),
                ('Unit', models.TextField(max_length=5)),
                ('Price3', models.DecimalField(decimal_places=2, default=0.0, max_digits=14)),
            ],
        ),
    ]
