from django.db import migrations, models

import company.models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_auto_20151016_1825'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name': 'Producent', 'verbose_name_plural': 'Producenci'},
        ),
        migrations.AlterField(
            model_name='company',
            name='common_name',
            field=models.CharField(max_length=128, verbose_name='Nazwa dla u\u017cytkownika', blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(
                db_index=True, max_length=128, null=True, verbose_name='Nazwa (pobrana z ILiM)', blank=True
            ),
        ),
        migrations.AlterField(
            model_name='company',
            name='nip',
            field=models.CharField(db_index=True, max_length=10, null=True, verbose_name='NIP/Tax ID', blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='official_name',
            field=models.CharField(max_length=128, null=True, verbose_name='Nazwa rejestrowa', blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='plCapital',
            field=company.models.IntegerRangeField(
                null=True, verbose_name='Udzia\u0142 polskiego kapita\u0142u', blank=True
            ),
        ),
        migrations.AlterField(
            model_name='company',
            name='plCapital_notes',
            field=models.TextField(
                null=True, verbose_name='Wi\u0119cej nt. udzia\u0142u polskiego kapita\u0142u', blank=True
            ),
        ),
        migrations.AlterField(
            model_name='company',
            name='plNotGlobEnt',
            field=company.models.IntegerRangeField(
                blank=True,
                null=True,
                verbose_name='Struktura kapita\u0142owa',
                choices=[
                    (0, '0 - Firma jest cz\u0119\u015bci\u0105 zagranicznego koncernu'),
                    (100, '100 - Firma nie jest cz\u0119\u015bci\u0105 zagranicznego koncernu'),
                ],
            ),
        ),
        migrations.AlterField(
            model_name='company',
            name='plNotGlobEnt_notes',
            field=models.TextField(null=True, verbose_name='Wi\u0119cej nt. struktury kapita\u0142owej', blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='plRegistered',
            field=company.models.IntegerRangeField(
                blank=True,
                null=True,
                verbose_name='Miejsce rejestracji',
                choices=[
                    (0, '0 - Firma zarejestrowana za granic\u0105'),
                    (100, '100 - Firma zarejestrowana w Polsce'),
                ],
            ),
        ),
        migrations.AlterField(
            model_name='company',
            name='plRegistered_notes',
            field=models.TextField(null=True, verbose_name='Wi\u0119cej nt. miejsca rejestracji', blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='plRnD',
            field=company.models.IntegerRangeField(
                blank=True,
                null=True,
                verbose_name='Wysokop\u0142atne miejsca pracy',
                choices=[
                    (0, '0 - Nie tworzy wysokop\u0142atnych miejsc pracy w Polsce'),
                    (100, '100 - Tworzy wysokop\u0142atne miejsca pracy w Polsce'),
                ],
            ),
        ),
        migrations.AlterField(
            model_name='company',
            name='plRnD_notes',
            field=models.TextField(
                null=True, verbose_name='Wi\u0119cej nt. wysokop\u0142atnych miejsc pracy', blank=True
            ),
        ),
        migrations.AlterField(
            model_name='company',
            name='plWorkers',
            field=company.models.IntegerRangeField(
                blank=True,
                null=True,
                verbose_name='Miejsce produkcji',
                choices=[(0, '0 - Nie produkuje w Polsce'), (100, '100 - Produkuje w Polsce')],
            ),
        ),
        migrations.AlterField(
            model_name='company',
            name='plWorkers_notes',
            field=models.TextField(null=True, verbose_name='Wi\u0119cej nt. miejsca produkcji', blank=True),
        ),
    ]
