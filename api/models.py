from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    made_in_poland = models.IntegerField(null=True, default=None, blank=True,
                                         validators=[MinValueValidator(0), MaxValueValidator(100)],
                                         verbose_name="Made in Poland (0-100%)")
    made_in_poland_info = models.TextField(blank=True)
    capital_in_poland = models.IntegerField(null=True, default=None, blank=True,
                                            validators=[MinValueValidator(0), MaxValueValidator(100)],
                                            verbose_name="Capital in Poland (0-100%)")
    capital_in_poland_info = models.TextField(blank=True)
    taxes_in_poland = models.IntegerField(null=True, default=None, blank=True,
                                          validators=[MinValueValidator(0), MaxValueValidator(100)],
                                          verbose_name="Taxes paid in Poland (0-100%)")
    taxes_in_poland_info = models.TextField(blank=True)
    krs_url = models.URLField(null=True)


class Product(models.Model):
    barcode = models.CharField(max_length=13)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    company = models.ForeignKey(Company)
    made_in_poland = models.IntegerField(null=True, default=None, blank=True,
                                         validators=[MinValueValidator(0), MaxValueValidator(100)],
                                         verbose_name="Made in Poland (0-100%)")
    made_in_poland_info = models.TextField(blank=True)
