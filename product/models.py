from django.core.urlresolvers import reverse
from django.db import models, transaction
from django.db.models import Count
from company.models import Company
import reversion
from model_utils.managers import PassThroughManager
from django.utils.translation import ugettext_lazy as _

class ProductQuerySet(models.query.QuerySet):
    def __init__(self, *args, **kwargs):
        super(ProductQuerySet, self).__init__(*args, **kwargs)

    def create(self, commit_desc=None, commit_user=None, *args, **kwargs):
        if not commit_desc:
            return super(ProductQuerySet, self).create(*args, **kwargs)

        with transaction.atomic(), reversion.create_revision(manage_manually=True):
            obj = super(ProductQuerySet, self).create(*args, **kwargs)
            reversion.default_revision_manager.save_revision([obj],
                comment=commit_desc, user=commit_user)
            return obj

    def with_query_count(self):
        return self.annotate(query_count=Count('query__id'))


class Product(models.Model):
    name = models.CharField(max_length=255, null=True)
    code = models.CharField(max_length=20, db_index=True)
    company = models.ForeignKey(Company, null=True, blank=True)

    objects = PassThroughManager.for_queryset_class(ProductQuerySet)()

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
