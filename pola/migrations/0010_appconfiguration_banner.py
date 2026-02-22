# Squashed migration for AppConfiguration banner fields

import django_resized.forms
from django.db import migrations, models

import pola.models
import pola.storages


class Migration(migrations.Migration):

    replaces = [
        ('pola', '0010_appconfiguration_default_banner'),
        ('pola', '0011_appconfiguration_banner_url'),
        ('pola', '0012_alter_appconfiguration_default_banner'),
        ('pola', '0013_alter_appconfiguration_banner'),
    ]

    dependencies = [
        ('pola', '0009_appconfiguration'),
    ]

    operations = [
        # Final state after 0013: add both fields with their latest definitions
        migrations.AddField(
            model_name='appconfiguration',
            name='banner_url',
            field=models.URLField(
                blank=True,
                max_length=255,
                null=True,
                verbose_name='Baner URL',
            ),
        ),
        migrations.AddField(
            model_name='appconfiguration',
            name='default_banner',
            field=django_resized.forms.ResizedImageField(
                blank=True,
                crop=None,
                force_format='PNG',
                keep_meta=True,
                null=True,
                quality=-1,
                scale=None,
                size=[1200, None],
                storage=pola.storages.OverwriteS3Boto3Storage(
                    bucket_name='pola-app-company-logotype',
                    default_acl=None,
                    querystring_auth=False,
                    region_name='eu-central-1',
                ),
                upload_to=pola.models.app_default_banner_upload_to,
                verbose_name='Domyślny baner',
            ),
        ),
    ]
