# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0002_auto_20141224_0017'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalCompany',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=255)),
                ('created_date', models.DateTimeField(editable=False, blank=True)),
                ('updated_date', models.DateTimeField(editable=False, blank=True)),
                ('made_in_poland', models.IntegerField(default=None, null=True, verbose_name=b'Made in Poland (0-100%)', blank=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('made_in_poland_info', models.TextField(blank=True)),
                ('capital_in_poland', models.IntegerField(default=None, null=True, verbose_name=b'Capital in Poland (0-100%)', blank=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('capital_in_poland_info', models.TextField(blank=True)),
                ('taxes_in_poland', models.IntegerField(default=None, null=True, verbose_name=b'Taxes paid in Poland (0-100%)', blank=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('taxes_in_poland_info', models.TextField(blank=True)),
                ('krs_url', models.URLField(null=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'verbose_name': 'historical company',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalProduct',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('barcode', models.CharField(max_length=13, db_index=True)),
                ('created_date', models.DateTimeField(editable=False, blank=True)),
                ('updated_date', models.DateTimeField(editable=False, blank=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('company_id', models.IntegerField(db_index=True, null=True, blank=True)),
                ('made_in_poland', models.IntegerField(default=None, null=True, verbose_name=b'Made in Poland (0-100%)', blank=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('made_in_poland_info', models.TextField(blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'verbose_name': 'historical product',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='product',
            name='barcode',
            field=models.CharField(max_length=13, db_index=True),
        ),
    ]
