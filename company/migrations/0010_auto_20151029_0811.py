from django.db import migrations, models

import company.models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0009_company_editor_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='plRnD',
            field=company.models.IntegerRangeField(
                blank=True,
                null=True,
                verbose_name='Miejsca pracy w BiR w Polsce',
                choices=[
                    (0, '0 - Nie tworzy miejsc pracy w BiR Polsce'),
                    (100, '100 - Tworzy miejsca pracy w BiR w Polsce'),
                ],
            ),
        ),
        migrations.AlterField(
            model_name='company',
            name='plRnD_notes',
            field=models.TextField(null=True, verbose_name='Wi\u0119cej nt. miejsc pracy w BiR', blank=True),
        ),
    ]
