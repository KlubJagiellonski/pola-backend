from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Count
from django.conf import settings
from company.models import Company
import reversion
from model_utils.managers import PassThroughManager
from produkty_w_sieci_api import Client, ApiError


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
        import ipdb; ipdb.set_trace()
        try:
            return cls.objects.get(code=code)
        except cls.DoesNotExist:
            try:
                product_info = Product._query_api(code)
                return Product.create_from_api(code, product_info)
            except ApiError:
                pass
        return cls.DoesNotExist(
                    "%s matching query does not exist." %
                    cls._meta.object_name
                 )

    @staticmethod
    def create_from_api(code, obj):
        import ipdb; ipdb.set_trace()
        company_name = obj.get('Data', {}).get('Owner', {}).get('Name', None)
        if company_name:
            company, _ = Company.objects.get_or_create(name=company_name)
        else:
            company = None
        name = obj.get('Data', {}).get('Product', {}).get('Name', None)
        return Product.objects.create(
            name=name,
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
        return self.name

reversion.register(Product)
