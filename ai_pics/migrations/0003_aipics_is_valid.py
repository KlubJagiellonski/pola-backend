from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai_pics', '0002_aiattachment_file_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='aipics',
            name='is_valid',
            field=models.NullBooleanField(),
        ),
    ]
