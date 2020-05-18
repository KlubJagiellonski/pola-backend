from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0002_auto_20151013_2305'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='desciption',
            new_name='description',
        ),
    ]
