# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='capital_in_poland',
            field=models.IntegerField(default=None, null=True, verbose_name=b'Capital in Poland (0-100%)', blank=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='company',
            name='made_in_poland',
            field=models.IntegerField(default=None, null=True, verbose_name=b'Made in Poland (0-100%)', blank=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='company',
            name='taxes_in_poland',
            field=models.IntegerField(default=None, null=True, verbose_name=b'Taxes paid in Poland (0-100%)', blank=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='product',
            name='made_in_poland',
            field=models.IntegerField(default=None, null=True, verbose_name=b'Made in Poland (0-100%)', blank=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
