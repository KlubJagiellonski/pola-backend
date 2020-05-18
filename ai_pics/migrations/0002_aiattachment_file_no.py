from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai_pics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='aiattachment',
            name='file_no',
            field=models.IntegerField(default=0),
        ),
    ]
