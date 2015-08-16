from django.db import models
from company.models import Company
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
import reversion


class Product(models.Model):
    name = models.CharField(max_length=32, null=True)
    code = models.CharField(max_length=20, db_index=True)
    company = models.ForeignKey(Company, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('product:detail', args=[self.code])

    def get_image_url(self):
        return reverse('product:image', args=[self.code])

    def __unicode__(self):
        return self.name

reversion.register(Product)
