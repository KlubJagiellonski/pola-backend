from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0021_product_replacements'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='replacements',
            field=models.ManyToManyField(
                blank=True,
                related_name='replaced_by',
                symmetrical=False,
                to='product.product',
                verbose_name='Zamienniki',
            ),
        ),
    ]
