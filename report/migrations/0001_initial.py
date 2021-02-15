from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                (
                    'id',
                    models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
                ),
                ('attachment', models.FileField(upload_to='reports/%Y/%m/%d', verbose_name='File')),
            ],
            options={
                'verbose_name': "Report's attachment",
                'verbose_name_plural': "Report's attachments",
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                (
                    'id',
                    models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
                ),
                ('client', models.CharField(default=None, max_length=40, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('resolved_at', models.DateTimeField(null=True, blank=True)),
                ('desciption', models.TextField()),
                ('product', models.ForeignKey(to='product.Product', on_delete=models.CASCADE)),
                (
                    'resolved_by',
                    models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE),
                ),
            ],
            options={
                'verbose_name': 'Report',
                'verbose_name_plural': 'Reports',
            },
        ),
        migrations.AddField(
            model_name='attachment',
            name='report',
            field=models.ForeignKey(to='report.Report', on_delete=models.CASCADE),
        ),
    ]
