from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20151025_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='code',
            field=models.CharField(unique=True, max_length=20, verbose_name='Kod', db_index=True),
        ),
    ]
