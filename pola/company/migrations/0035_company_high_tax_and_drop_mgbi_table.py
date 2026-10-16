from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('company', '0034_alter_company_logotype'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='high_tax',
            field=models.BooleanField(default=False),
        ),
        migrations.RunSQL(
            sql="DROP TABLE IF EXISTS mgbidatamodel;",
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
