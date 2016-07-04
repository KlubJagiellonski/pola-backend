from django.core.urlresolvers import reverse
from django.db import models

from company.models import Company


class Brand(models.Model):
    company = models.ForeignKey(Company, null=True)
    name = models.CharField(max_length=128, null=True, blank=True,
                            verbose_name="Nazwa marki")

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        if self.company_id:
            return reverse('company:detail', args=[self.company_id])
        return None
