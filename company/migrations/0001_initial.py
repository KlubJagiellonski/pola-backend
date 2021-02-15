from django.db import migrations, models

import company.models


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                (
                    'id',
                    models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
                ),
                (
                    'nip',
                    models.CharField(
                        db_index=True, max_length=10, null=True, verbose_name="Company's NIP#", blank=True
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        db_index=True,
                        max_length=128,
                        null=True,
                        verbose_name='Name as retrieved from produkty_w_sieci API',
                        blank=True,
                    ),
                ),
                (
                    'official_name',
                    models.CharField(max_length=128, null=True, verbose_name='Official company name', blank=True),
                ),
                (
                    'common_name',
                    models.CharField(max_length=128, verbose_name='Common company name', blank=True),
                ),
                ('address', models.TextField(null=True, blank=True)),
                (
                    'plCapital',
                    company.models.IntegerRangeField(
                        null=True, verbose_name='Percentage share of Polish capital', blank=True
                    ),
                ),
                (
                    'plCapital_notes',
                    models.TextField(null=True, verbose_name='Notes about share of Polish capital', blank=True),
                ),
                (
                    'plTaxes',
                    company.models.IntegerRangeField(
                        null=True,
                        verbose_name='Payment of taxes and information about registration',
                        blank=True,
                    ),
                ),
                (
                    'plTaxes_notes',
                    models.TextField(null=True, verbose_name='Notes about payment of taxes', blank=True),
                ),
                (
                    'plRnD',
                    company.models.IntegerRangeField(
                        null=True, verbose_name='Information about R&D center', blank=True
                    ),
                ),
                (
                    'plRnD_notes',
                    models.TextField(null=True, verbose_name='Notes about R&D center', blank=True),
                ),
                (
                    'plWorkers',
                    company.models.IntegerRangeField(null=True, verbose_name='Information about workers', blank=True),
                ),
                (
                    'plWorkers_notes',
                    models.TextField(null=True, verbose_name='Notes about workers', blank=True),
                ),
                (
                    'plBrand',
                    company.models.IntegerRangeField(null=True, verbose_name='Information about brand', blank=True),
                ),
                ('plBrand_notes', models.TextField(null=True, verbose_name='Notes about brand', blank=True)),
                ('verified', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Company',
                'verbose_name_plural': 'Companies',
            },
        ),
    ]
