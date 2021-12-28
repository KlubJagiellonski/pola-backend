from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                (
                    'id',
                    models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
                ),
                ('name', models.CharField(max_length=255, null=True)),
                ('code', models.CharField(max_length=20, db_index=True)),
                (
                    'company',
                    models.ForeignKey(blank=True, to='company.Company', null=True, on_delete=models.CASCADE),
                ),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
    ]
