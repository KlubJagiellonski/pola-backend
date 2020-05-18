from django.db import migrations, models

import company.models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='plBrand',
        ),
        migrations.RemoveField(
            model_name='company',
            name='plBrand_notes',
        ),
        migrations.RemoveField(
            model_name='company',
            name='plTaxes',
        ),
        migrations.RemoveField(
            model_name='company',
            name='plTaxes_notes',
        ),
        migrations.AddField(
            model_name='company',
            name='plNotGlobEnt',
            field=company.models.IntegerRangeField(null=True, verbose_name="Isn't it a global enterprise?", blank=True),
        ),
        migrations.AddField(
            model_name='company',
            name='plNotGlobEnt_notes',
            field=models.TextField(null=True, verbose_name='Notes about global enterprise', blank=True),
        ),
        migrations.AddField(
            model_name='company',
            name='plRegistered',
            field=company.models.IntegerRangeField(null=True, verbose_name='Registered in Poland?', blank=True),
        ),
        migrations.AddField(
            model_name='company',
            name='plRegistered_notes',
            field=models.TextField(null=True, verbose_name='Notes about registered in Poland', blank=True),
        ),
    ]
