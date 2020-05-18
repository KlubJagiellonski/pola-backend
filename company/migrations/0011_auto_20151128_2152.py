from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0010_auto_20151029_0811'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='description',
            field=models.TextField(null=True, verbose_name='Opis producenta', blank=True),
        ),
        migrations.AddField(
            model_name='company',
            name='sources',
            field=models.TextField(null=True, verbose_name='\u0179r\xf3d\u0142a', blank=True),
        ),
    ]
