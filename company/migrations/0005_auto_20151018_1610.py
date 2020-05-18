from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_auto_20151018_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='verified',
            field=models.BooleanField(default=False, verbose_name='Dane zweryfikowane'),
        ),
    ]
