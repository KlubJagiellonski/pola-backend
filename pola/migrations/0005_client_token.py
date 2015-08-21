# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import binascii
import os

from django.db import models, migrations


def gen_token(apps, schema_editor):
    ClientModel = apps.get_model('pola', 'Client')
    for row in ClientModel.objects.all():
        row.token = binascii.hexlify(os.urandom(20)).decode()
        row.save()


class Migration(migrations.Migration):

    dependencies = [
        ('pola', '0004_query_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='token',
            field=models.CharField(default=None, max_length=40, unique=True, null=True, blank=True),
        ),
        migrations.RunPython(gen_token, reverse_code=migrations.RunPython.noop)
    ]
