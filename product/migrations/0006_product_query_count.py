from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_product_ilim_queried_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='query_count',
            field=models.PositiveIntegerField(default=0, db_index=True),
        ),
    ]
