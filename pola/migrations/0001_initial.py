# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Barcode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=20, db_index=True)),
                ('event_desc', models.CharField(max_length=30, null=True)),
                ('description_of_change', models.TextField(max_length=64, verbose_name='Description of change')),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
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
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(to='pola.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('desciption', models.TextField()),
                ('barcode', models.ForeignKey(to='pola.Barcode')),
                ('client', models.ForeignKey(to='pola.Client')),
            ],
        ),
        migrations.AddField(
            model_name='barcode',
            name='company',
            field=models.ForeignKey(to='pola.Company', null=True),
        ),
    ]
