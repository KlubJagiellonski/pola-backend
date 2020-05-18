from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pola', '0003_auto_20151025_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='stats',
            name='no_of_not_verified_590',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='stats',
            name='no_of_not_verified_not_590',
            field=models.IntegerField(default=0),
        ),
    ]
