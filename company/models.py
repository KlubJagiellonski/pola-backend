from django.core.urlresolvers import reverse
from django.db import models, transaction
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

    def get_or_create(self, commit_desc=None, *args, **kwargs):
        if not commit_desc:
            return super(CompanyQuerySet, self).get_or_create(*args, **kwargs)

        with transaction.atomic(), reversion.create_revision():
            obj = super(CompanyQuerySet, self).get_or_create(*args, **kwargs)
            reversion.set_comment(commit_desc)
            return obj

    def with_query_count(self):
        return self.annotate(query_count=Count('product__query__id'))


class Company(models.Model):
    nip = models.CharField(max_length=10, db_index=True, null=True, blank=True)
    name = models.CharField(max_length=64, null=True, blank=True)
    official_name = models.CharField(max_length=64, blank=True, null=True)
    address = models.TextField(null=True, blank=True)
    plCapital = IntegerRangeField(
        verbose_name=_("Percentage share of Polish capital"),
        min_value=0, max_value=100, null=True, blank=True)
    plCapital_notes = models.TextField(
        _("Notes about share of Polish capital"), null=True, blank=True)
    plTaxes = IntegerRangeField(
        verbose_name=_("Payment of taxes and information about registration"),
        min_value=0, max_value=100, null=True, blank=True)
    plTaxes_notes = models.TextField(
        _("Notes about payment of taxes"), null=True, blank=True)
    plRnD = IntegerRangeField(
        verbose_name=_("Information about R&D center"),
        min_value=0, max_value=100, null=True, blank=True)
    plRnD_notes = models.TextField(
        _("Notes about R&D center"), null=True, blank=True)
    plWorkers = IntegerRangeField(
        verbose_name=_("Information about workers"),
        min_value=0, max_value=100, null=True, blank=True)
    plWorkers_notes = models.TextField(
        _("Notes about workers"), null=True, blank=True)
    plBrand = IntegerRangeField(
        verbose_name=_("Information about brand"),
        min_value=0, max_value=100, null=True, blank=True)
    plBrand_notes = models.TextField(
        _("Notes about brand"), null=True, blank=True)
    verified = models.BooleanField(default=False)

    objects = PassThroughManager.for_queryset_class(CompanyQuerySet)()

    def to_dict(self):
        dict = model_to_dict(self)
        return dict

    def get_absolute_url(self):
        return reverse('company:detail', args=[self.pk])

    def __unicode__(self):
        return self.name or self.official_name

    def save(self, commit_desc=None, *args, **kwargs):
        if not commit_desc:
            return super(Company, self).save(*args, **kwargs)

        with transaction.atomic(), reversion.create_revision():
            obj = super(Company, self).save(*args, **kwargs)
            reversion.set_comment(commit_desc)
            return obj

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")

reversion.register(Company)
