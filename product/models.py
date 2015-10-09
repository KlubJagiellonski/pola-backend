from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Count
from django.conf import settings
from company.models import Company
import reversion
from model_utils.managers import PassThroughManager
from produkty_w_sieci_api import Client, ApiError
from django.utils.translation import ugettext_lazy as _
from mojepanstwo_api import KrsClient, CompanyNotFound, ApiError


class ProductQuerySet(models.query.QuerySet):
    def __init__(self, *args, **kwargs):
        super(ProductQuerySet, self).__init__(*args, **kwargs)

    def with_query_count(self):
        return self.annotate(query_count=Count('query__id'))


class Product(models.Model):
    name = models.CharField(max_length=255, null=True)
    code = models.CharField(max_length=20, db_index=True)
    company = models.ForeignKey(Company, null=True, blank=True)

    objects = PassThroughManager.for_queryset_class(ProductQuerySet)()

    @classmethod
    def get_by_code(cls, code):
        try:
            return cls.objects.get(code=code)
        except cls.DoesNotExist:
            pass
        try:
            product_info = Product._query_api(code)
            return Product.create_from_api(code, product_info)
        except ApiError:
            pass
        return Product.objects.create(code=code)

    @staticmethod
    def create_from_api(code, obj):
        obj_data = obj.get('Data', {}) or {}
        obj_owner = obj_data.get('Owner', {}) or {}
        obj_owner_name = obj_owner.get('Name', None)
        obj_product = obj.get('Product', {}) or {}
        obj_product_name = obj_product.get('Name', None)

        try:
            krs = KrsClient()
            companies = krs.get_companies_by_name()
        except (CompanyNotFound, ApiError):
            pass

        if obj_owner_name:
            company, _ = Company.objects.get_or_create(name=obj_owner_name)
        else:
            company = None
        return Product.objects.create(
            name=obj_product_name,
            code=code,
            company=company)

    @staticmethod
    def _query_api(code):
        client = Client(settings.PRODUKTY_W_SIECI_API_KEY)
        return client.get_product_by_gtin(code)

    def get_absolute_url(self):
        return reverse('product:detail', args=[self.code])

    def get_image_url(self):
        return reverse('product:image', args=[self.code])

    def __unicode__(self):
        return self.name or self.code or "None"

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

reversion.register(Product)
