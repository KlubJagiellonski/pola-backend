from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0011_auto_20151128_2152'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='query_count',
            field=models.PositiveIntegerField(default=0, db_index=True),
        ),
    ]
