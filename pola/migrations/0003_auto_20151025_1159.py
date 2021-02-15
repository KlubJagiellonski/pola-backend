from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pola', '0002_auto_20151022_1712'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stats',
            fields=[
                (
                    'id',
                    models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
                ),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('day', models.IntegerField()),
                ('calculated_at', models.DateTimeField(auto_now_add=True)),
                ('no_of_queries', models.IntegerField()),
                ('no_of_clients', models.IntegerField()),
                ('no_of_verified', models.IntegerField()),
                ('no_of_plScore', models.IntegerField()),
                ('no_of_590', models.IntegerField()),
                ('no_of_new_companies', models.IntegerField()),
                ('no_of_new_products', models.IntegerField()),
                ('no_of_new_reports', models.IntegerField()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='stats',
            unique_together={('year', 'month', 'day')},
        ),
    ]
