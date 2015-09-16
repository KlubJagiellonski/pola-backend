from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Count
from django.forms.models import model_to_dict
from django.utils.translation import ugettext_lazy as _
from model_utils.managers import PassThroughManager
import reversion


class IntegerRangeField(models.IntegerField):
    def __init__(self, min_value=None, max_value=None, *args, **kwargs):
        super(models.IntegerField, self).__init__(*args, **kwargs)
        self.min_value, self.max_value = min_value, max_value

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value,
                    'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class CompanyQuerySet(models.query.QuerySet):
    def with_query_count(self):
        return self.annotate(query_count=Count('product__query__id'))


class Company(models.Model):
    nip = models.CharField(max_length=10, db_index=True)
    name = models.CharField(max_length=64)
    address = models.TextField()
    plCapital = IntegerRangeField(
        verbose_name=_("Percentage share of Polish capital"),
        min_value=1, max_value=100, null=True, blank=True)
    plCapital_notes = models.TextField(
        _("Notes about share of Polish capital"), null=True)

    objects = PassThroughManager.for_queryset_class(CompanyQuerySet)()

    def to_dict(self):
        dict = model_to_dict(self)
        return dict

    def get_absolute_url(self):
        return reverse('company:detail', args=[self.pk])

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"

reversion.register(Company)
