from django.db import models
from product.models import Product
# from django.core.urlresolvers import reverse


class Query(models.Model):
    client = models.CharField(max_length=40,
                              blank=True, null=True, default=None)
    product = models.ForeignKey(Product)
    timestamp = models.DateTimeField(auto_now_add=True)
