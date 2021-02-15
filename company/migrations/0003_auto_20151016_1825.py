from django.db import migrations, models

import company.models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_auto_20151015_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='plNotGlobEnt',
            field=company.models.IntegerRangeField(
                blank=True,
                null=True,
                verbose_name="Isn't it a global enterprise?",
                choices=[(0, 0), (100, 100)],
            ),
        ),
        migrations.AlterField(
            model_name='company',
            name='plRegistered',
            field=company.models.IntegerRangeField(
                blank=True, null=True, verbose_name='Registered in Poland?', choices=[(0, 0), (100, 100)]
            ),
        ),
        migrations.AlterField(
            model_name='company',
            name='plRegistered_notes',
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name='Notes about registered in Poland',
                choices=[(0, 0), (100, 100)],
            ),
        ),
        migrations.AlterField(
            model_name='company',
            name='plRnD',
            field=company.models.IntegerRangeField(
                blank=True,
                null=True,
                verbose_name='Information about R&D center',
                choices=[(0, 0), (100, 100)],
            ),
        ),
        migrations.AlterField(
            model_name='company',
            name='plWorkers',
            field=company.models.IntegerRangeField(
                blank=True, null=True, verbose_name='Information about workers', choices=[(0, 0), (100, 100)]
            ),
        ),
    ]
