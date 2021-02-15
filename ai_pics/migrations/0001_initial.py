from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_product_query_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='AIAttachment',
            fields=[
                (
                    'id',
                    models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
                ),
                ('attachment', models.FileField(upload_to='ai/%Y/%m/%d', verbose_name='File')),
            ],
            options={
                'verbose_name': "AIPics's attachment",
                'verbose_name_plural': "AIPics's attachments",
            },
        ),
        migrations.CreateModel(
            name='AIPics',
            fields=[
                (
                    'id',
                    models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
                ),
                ('client', models.CharField(max_length=40, verbose_name='Zg\u0142aszaj\u0105cy')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Utworzone')),
                ('original_width', models.IntegerField()),
                ('original_height', models.IntegerField()),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
                ('device_name', models.CharField(max_length=100)),
                ('flash_used', models.NullBooleanField()),
                ('was_portrait', models.NullBooleanField()),
                ('product', models.ForeignKey(to='product.Product', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'AIPics',
                'verbose_name_plural': 'AIPics',
            },
        ),
        migrations.AddField(
            model_name='aiattachment',
            name='ai_pics',
            field=models.ForeignKey(to='ai_pics.AIPics', on_delete=models.CASCADE),
        ),
    ]
