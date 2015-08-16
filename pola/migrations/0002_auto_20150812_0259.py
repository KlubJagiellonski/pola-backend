# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pola', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('code', models.CharField(max_length=20, db_index=True)),
                ('event_desc', models.CharField(max_length=30, null=True)),
                ('description_of_change', models.TextField(max_length=64, verbose_name='Description of change')),
                ('company', models.ForeignKey(to='pola.Company', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='barcode',
            name='company',
        ),
        migrations.AlterField(
            model_name='report',
            name='barcode',
            field=models.ForeignKey(to='pola.Product'),
        ),
        migrations.DeleteModel(
            name='Barcode',
        ),
    ]
