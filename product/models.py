from django.contrib.postgres.indexes import BrinIndex
from django.core import validators
from django.db import connection, models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from reversion import revisions as reversion

from company.models import Brand, Company
from pola.concurency import concurency


class ProductQuerySet(models.query.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create(self, commit_desc=None, commit_user=None, *args, **kwargs):
        if not commit_desc:
            return super().create(*args, **kwargs)

        with reversion.create_revision(manage_manually=True, atomic=True):
            obj = super().create(*args, **kwargs)
            reversion.set_comment(commit_desc)
            reversion.set_user(commit_user)
            reversion.add_to_revision(obj)
            return obj


@reversion.register
class Product(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    ilim_queried_at = models.DateTimeField(default=timezone.now, null=False)
    name = models.CharField(max_length=255, null=True, verbose_name="Nazwa")
    code = models.CharField(
        max_length=20, db_index=True, verbose_name="Kod", unique=True, validators=[validators.validate_integer]
    )
    company = models.ForeignKey(Company, null=True, blank=True, verbose_name="Producent", on_delete=models.CASCADE)
    companies = models.ManyToManyField(Company, verbose_name="Producenci", related_name='companies')
    brand = models.ForeignKey(Brand, null=True, blank=True, verbose_name="Marka produktu", on_delete=models.CASCADE)
    query_count = models.PositiveIntegerField(null=False, default=0, db_index=True)
    ai_pics_count = models.PositiveIntegerField(null=False, default=0)

    objects = ProductQuerySet.as_manager()

    def get_absolute_url(self):
        return reverse('product:detail', args=[self.code])

    def locked_by(self):
        return concurency.locked_by(self)

    def get_image_url(self):
        return reverse('product:image', args=[self.code])

    def __str__(self):
        return self.name or self.code or "None"

    def save(self, commit_desc=None, commit_user=None, *args, **kwargs):
        if not commit_desc:
            super().save(*args, **kwargs)
            return

        with reversion.create_revision(manage_manually=True, atomic=True):
            super().save(*args, **kwargs)
            reversion.set_comment(commit_desc)
            reversion.set_user(commit_user)
            reversion.add_to_revision(self)

    def increment_query_count(self):
        with connection.cursor() as cursor:
            cursor.execute('update product_product set query_count = query_count +1 ' 'where id=%s', [self.id])

    def increment_ai_pics_count(self):
        with connection.cursor() as cursor:
            cursor.execute('update product_product set ai_pics_count = ai_pics_count +1 ' 'where id=%s', [self.id])

    @staticmethod
    def recalculate_query_count():
        with connection.cursor() as cursor:
            cursor.execute(
                'update product_product set query_count = (select count(id) '
                'from pola_query '
                'where pola_query.product_id=product_product.id)'
            )

    @staticmethod
    def recalculate_ai_pics_count():
        with connection.cursor() as cursor:
            cursor.execute(
                'update product_product set ai_pics_count = (select count(id) '
                'from ai_pics_aipics '
                'where ai_pics_aipics.product_id=product_product.id and '
                '(ai_pics_aipics.is_valid=TRUE or ai_pics_aipics.is_valid IS NULL))'
            )

    class Meta:
        verbose_name = _("Produkt")
        verbose_name_plural = _("Produkty")
        ordering = ['-created_at']
        permissions = (
            # ("view_product", "Can see all product"),
            # ("add_product", "Can add a new product"),
            # ("change_product", "Can edit the product"),
            # ("delete_product", "Can delete the product"),
        )
        indexes = [BrinIndex(fields=['created_at'], pages_per_range=16)]
