import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0007_auto_20151021_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='created_at',
            field=models.DateTimeField(
                default=datetime.datetime(2015, 10, 25, 10, 59, 15, 308311, tzinfo=utc), auto_now_add=True
            ),
            preserve_default=False,
        ),
    ]
