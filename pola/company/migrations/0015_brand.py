import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0014_auto_20180527_0848'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                (
                    'id',
                    models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                (
                    'name',
                    models.CharField(
                        blank=True,
                        db_index=True,
                        max_length=128,
                        null=True,
                        verbose_name='Nazwa marki (na podstawie ILiM)',
                    ),
                ),
                (
                    'common_name',
                    models.CharField(blank=True, max_length=128, null=True, verbose_name='Nazwa dla użytkownika'),
                ),
                (
                    'company',
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='company.Company'),
                ),
            ],
            options={
                'verbose_name': 'Marka',
                'verbose_name_plural': 'Marki',
                'ordering': ['-created_at'],
                'permissions': (('view_brand', 'Can see all brands'),),
            },
        ),
    ]
