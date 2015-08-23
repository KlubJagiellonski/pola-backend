from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Count
from company.models import Company
import reversion
from model_utils.managers import PassThroughManager


class ProductQuerySet(models.query.QuerySet):
    def __init__(self, *args, **kwargs):
        super(ProductQuerySet, self).__init__(*args, **kwargs)

    def with_query_count(self):
        return self.annotate(query_count=Count('query__id'))


class Product(models.Model):
    name = models.CharField(max_length=32, null=True)
    code = models.CharField(max_length=20, db_index=True)
    company = models.ForeignKey(Company, null=True, blank=True)

    objects = PassThroughManager.for_queryset_class(ProductQuerySet)()

    def get_absolute_url(self):
        return reverse('product:detail', args=[self.code])

    def get_image_url(self):
        return reverse('product:image', args=[self.code])

    def __unicode__(self):
        return self.name

reversion.register(Product)
