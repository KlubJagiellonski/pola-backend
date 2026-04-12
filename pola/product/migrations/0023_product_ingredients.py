from django.db import migrations, models
from django.utils.translation import gettext_lazy as _


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0022_alter_product_replacements_asym'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='ingredients',
            field=models.CharField(
                choices=[('PL', _('Polskie surowce')), ('NPL', _('Nie polskie surowce'))],
                default=None,
                blank=True,
                max_length=3,
                null=True,
                verbose_name=_('Surowce'),
                help_text=_('Wybierz pochodzenie surowców; brak danych oznacza pustą wartość.'),
            ),
        ),
    ]
