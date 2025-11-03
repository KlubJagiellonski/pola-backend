from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0022_alter_product_replacements_asym'),
    ]

    operations = [
        migrations.RunSQL(
            sql=(
                "ALTER TABLE product_product_replacements " "ADD COLUMN IF NOT EXISTS counts integer NOT NULL DEFAULT 0"
            ),
            reverse_sql=("ALTER TABLE product_product_replacements " "DROP COLUMN IF EXISTS counts"),
        ),
    ]
