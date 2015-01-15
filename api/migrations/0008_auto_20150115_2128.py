# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20150110_1112'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='made_in_poland',
        ),
        migrations.RemoveField(
            model_name='company',
            name='made_in_poland_info',
        ),
        migrations.RemoveField(
            model_name='company',
            name='taxes_in_poland',
        ),
        migrations.RemoveField(
            model_name='company',
            name='taxes_in_poland_info',
        ),
        migrations.RemoveField(
            model_name='historicalcompany',
            name='made_in_poland',
        ),
        migrations.RemoveField(
            model_name='historicalcompany',
            name='made_in_poland_info',
        ),
        migrations.RemoveField(
            model_name='historicalcompany',
            name='taxes_in_poland',
        ),
        migrations.RemoveField(
            model_name='historicalcompany',
            name='taxes_in_poland_info',
        ),
    ]
