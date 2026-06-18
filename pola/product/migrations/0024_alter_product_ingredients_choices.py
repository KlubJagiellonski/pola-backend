from django.db import migrations, models
from django.utils.translation import gettext_lazy as _


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0023_product_ingredients'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='ingredients',
            field=models.CharField(
                choices=[
                    ('PL', _('Polskie surowce')),
                    ('NPL', _('Nie polskie surowce')),
                    ('DW', _('Do weryfikacji')),
                ],
                default=None,
                blank=True,
                max_length=3,
                null=True,
                verbose_name=_('Surowce'),
            ),
        ),
    ]
