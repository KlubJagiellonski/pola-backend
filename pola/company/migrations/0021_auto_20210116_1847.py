# Generated by Django 3.1.2 on 2021-01-16 17:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('company', '0020_auto_20210113_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='name',
            field=models.CharField(
                db_index=True, max_length=128, unique=False, verbose_name='Nazwa marki (na podstawie ILiM)'
            ),
        ),
    ]
