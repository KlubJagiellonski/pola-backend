from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='product',
            field=models.ForeignKey(to='product.Product', null=True, on_delete=models.CASCADE),
        ),
    ]
