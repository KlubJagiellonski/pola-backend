from django.db import models
from product.models import Product
from datetime import datetime, timedelta


class Query(models.Model):
    client = models.CharField(max_length=40,
                              blank=True, null=True, default=None)
    product = models.ForeignKey(Product)
    was_verified = models.BooleanField(default=False)
    was_plScore = models.BooleanField(default=False)
    was_590 = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

