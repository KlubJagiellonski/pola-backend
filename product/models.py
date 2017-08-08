from django.core.urlresolvers import reverse
from django.db import models, transaction, connection
from company.models import Company
import reversion
from django.utils.translation import ugettext_lazy as _
from pola.concurency import concurency
from django.utils import timezone


class ProductQuerySet(models.query.QuerySet):
    def __init__(self, *args, **kwargs):
        super(ProductQuerySet, self).__init__(*args, **kwargs)

    def create(self, commit_desc=None, commit_user=None, *args, **kwargs):
        if not commit_desc:
            return super(ProductQuerySet, self).create(*args, **kwargs)

        with transaction.atomic(), reversion.create_revision(manage_manually=True):
            obj = super(ProductQuerySet, self).create(*args, **kwargs)
            revision_manager = reversion.default_revision_manager
            revision_manager.save_revision([obj],
                                           comment=commit_desc,
                                           user=commit_user)
            return obj


class Product(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, )
    ilim_queried_at = models.DateTimeField(default=timezone.now, null=False)
    name = models.CharField(max_length=255, null=True, verbose_name="Nazwa")
    code = models.CharField(max_length=20, db_index=True, verbose_name="Kod",
                            unique=True)
    company = models.ForeignKey(Company, null=True, blank=True,
                                verbose_name="Producent")
    query_count = models.PositiveIntegerField(null=False, default=0, db_index=True)
    ai_pics_count = models.PositiveIntegerField(null=False, default=0)

    objects = ProductQuerySet.as_manager()

    def get_absolute_url(self):
        return reverse('product:detail', args=[self.code])

    def locked_by(self):
        return concurency.locked_by(self)

    def get_image_url(self):
        return reverse('product:image', args=[self.code])

    def __unicode__(self):
        return self.name or self.code or "None"

    def save(self, commit_desc=None, commit_user=None, *args, **kwargs):
        if not commit_desc:
            return super(Product, self).save(*args, **kwargs)

        with transaction.atomic(), reversion.\
                create_revision(manage_manually=True):
            obj = super(Product, self).save(*args, **kwargs)
            reversion.default_revision_manager.\
                save_revision([self], comment=commit_desc, user=commit_user)
            return obj

    def increment_query_count(self):
        with connection.cursor() as cursor:
            cursor.execute(
                'update product_product set query_count = query_count +1 '
                'where id=%s', [self.id])

    @staticmethod
    def recalculate_query_count():
        with connection.cursor() as cursor:
            cursor.execute(
                'update product_product set query_count = (select count(id) '
                'from pola_query '
                'where pola_query.product_id=product_product.id)')

    @staticmethod
    def recalculate_ai_pics_count():
        with connection.cursor() as cursor:
            cursor.execute(
                'update product_product set ai_pics_count = (select count(id) '
                'from ai_pics_aipics '
                'where ai_pics_aipics.product_id=product_product.id and '
                '(ai_pics_aipics.is_valid=TRUE or ai_pics_aipics.is_valid IS NULL))')


    class Meta:
        verbose_name = _("Produkt")
        verbose_name_plural = _("Produkty")

reversion.register(Product)
