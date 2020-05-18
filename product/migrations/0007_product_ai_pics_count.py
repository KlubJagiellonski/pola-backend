from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_product_query_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='ai_pics_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
