from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Query',
            fields=[
                (
                    'id',
                    models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
                ),
                ('client', models.CharField(default=None, max_length=40, null=True, blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(to='product.Product', on_delete=models.CASCADE)),
            ],
        ),
    ]
