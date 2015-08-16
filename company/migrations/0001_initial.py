# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nip', models.CharField(max_length=10, db_index=True)),
                ('name', models.CharField(max_length=64)),
                ('adres', models.TextField()),
                ('wspolnicy', jsonfield.fields.JSONField(null=True)),
                ('description_of_change', models.CharField(max_length=64)),
                ('plCapital', models.IntegerField(verbose_name='Percentage share of Polish capital')),
                ('plCapital_notes', models.TextField(null=True, verbose_name='Notes about share of Polish capital')),
            ],
            options={
                'verbose_name_plural': 'Companies',
            },
        ),
    ]
