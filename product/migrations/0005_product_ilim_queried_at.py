import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20151029_0811'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='ilim_queried_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
