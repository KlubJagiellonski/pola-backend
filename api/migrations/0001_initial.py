# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('made_in_poland', models.IntegerField(default=None, null=True, verbose_name=b'Made in Poland (0-100%)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('made_in_poland_info', models.TextField(blank=True)),
                ('capital_in_poland', models.IntegerField(default=None, null=True, verbose_name=b'Capital in Poland (0-100%)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('capital_in_poland_info', models.TextField(blank=True)),
                ('taxes_in_poland', models.IntegerField(default=None, null=True, verbose_name=b'Taxes paid in Poland (0-100%)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('taxes_in_poland_info', models.TextField(blank=True)),
                ('krs_url', models.URLField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('barcode', models.CharField(max_length=13)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('made_in_poland', models.IntegerField(default=None, null=True, verbose_name=b'Made in Poland (0-100%)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('made_in_poland_info', models.TextField(blank=True)),
                ('company', models.ForeignKey(to='api.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
