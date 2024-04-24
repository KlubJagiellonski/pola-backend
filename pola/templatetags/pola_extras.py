from django import template
from django.utils import numberformat

register = template.Library()


@register.filter
def intspace(value):
    return numberformat.format(
        number=value,
        decimal_sep=',',
        decimal_pos=None,
        grouping=3,
        thousand_sep=' ',
        force_grouping=True,
        use_l10n=None,
    )
