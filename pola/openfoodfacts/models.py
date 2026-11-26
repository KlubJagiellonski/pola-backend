from django.db import models


class ProductColumns(models.Model):
    code = models.TextField(primary_key=True)
    product_name = models.TextField(null=True, blank=True)
    generic_name = models.TextField(null=True, blank=True)
    brands = models.TextField(null=True, blank=True)
    quantity = models.TextField(null=True, blank=True)
    brands_tags = models.TextField(null=True, blank=True)
    categories_tags = models.TextField(null=True, blank=True)
    countries_tags = models.TextField(null=True, blank=True)
    allergens_tags = models.TextField(null=True, blank=True)
    traces_tags = models.TextField(null=True, blank=True)
    ingredients_text = models.TextField(null=True, blank=True)
    nutriscore_grade = models.TextField(null=True, blank=True)
    nova_group = models.IntegerField(null=True, blank=True)
    ecoscore_grade = models.TextField(null=True, blank=True)
    completeness = models.DecimalField(max_digits=14, decimal_places=4, null=True, blank=True)
    energy_kcal = models.DecimalField(max_digits=14, decimal_places=4, null=True, blank=True)
    fat = models.DecimalField(max_digits=14, decimal_places=4, null=True, blank=True)
    saturated_fat = models.DecimalField(max_digits=14, decimal_places=4, null=True, blank=True)
    carbohydrates = models.DecimalField(max_digits=14, decimal_places=4, null=True, blank=True)
    sugars = models.DecimalField(max_digits=14, decimal_places=4, null=True, blank=True)
    fiber = models.DecimalField(max_digits=14, decimal_places=4, null=True, blank=True)
    proteins = models.DecimalField(max_digits=14, decimal_places=4, null=True, blank=True)
    salt = models.DecimalField(max_digits=14, decimal_places=4, null=True, blank=True)
    image_url = models.TextField(null=True, blank=True)
    last_modified_t = models.BigIntegerField(null=True, blank=True)

    class Meta:
        abstract = True


class Product(ProductColumns):
    class Meta:
        db_table = 'openfoodfacts"."product'


class ProductNext(ProductColumns):
    class Meta:
        db_table = 'openfoodfacts"."product_next'


class LoadRun(models.Model):
    class Mode(models.TextChoices):
        FULL = 'full', 'full'
        DELTA = 'delta', 'delta'

    class Status(models.TextChoices):
        SUCCESS = 'success', 'success'
        FAILED = 'failed', 'failed'

    started_at = models.DateTimeField()
    finished_at = models.DateTimeField(null=True, blank=True)
    mode = models.CharField(max_length=8, choices=Mode.choices)
    source_url = models.TextField()
    sha256 = models.CharField(max_length=64, null=True, blank=True)
    delta_end_unix = models.BigIntegerField(null=True, blank=True)
    row_count = models.BigIntegerField(null=True, blank=True)
    status = models.CharField(max_length=16, choices=Status.choices)
    error = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'openfoodfacts"."load_run'
