from datetime import datetime, timedelta

from django.contrib.postgres.indexes import BrinIndex
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import get_default_timezone

from pola.company.models import Company
from pola.product.models import Product
from pola.report.models import Report


class Query(models.Model):
    client = models.CharField(max_length=40, blank=True, null=True, default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    was_verified = models.BooleanField(default=False)
    was_plScore = models.BooleanField(default=False)
    was_590 = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'timestamp'
        indexes = [BrinIndex(fields=['timestamp'], pages_per_range=64)]


class SearchQuery(models.Model):
    client = models.CharField(max_length=40, blank=True, null=True, default=None)
    text = models.CharField(max_length=255, blank=True, null=True, default=None)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'timestamp'
        indexes = [BrinIndex(fields=['timestamp'], pages_per_range=64)]


class Stats(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    calculated_at = models.DateTimeField(auto_now_add=True)
    no_of_queries = models.IntegerField()
    no_of_clients = models.IntegerField()
    no_of_verified = models.IntegerField()
    no_of_plScore = models.IntegerField()
    no_of_590 = models.IntegerField()
    no_of_not_verified_590 = models.IntegerField(default=0)
    no_of_not_verified_not_590 = models.IntegerField(default=0)
    no_of_new_companies = models.IntegerField()
    no_of_new_products = models.IntegerField()
    no_of_new_reports = models.IntegerField()

    def get_date(self):
        return '%d %s' % (
            self.day,
            datetime(self.year, self.month, self.day, tzinfo=get_default_timezone()).strftime('%b'),
        )

    class Meta:
        unique_together = ('year', 'month', 'day')
        indexes = [BrinIndex(fields=['calculated_at'], pages_per_range=16)]

    def calculate(self, year, month, day):
        today_midnight = datetime(year, month, day, tzinfo=get_default_timezone())
        tomorrow_midnight = today_midnight + timedelta(days=1)

        self.year = year
        self.month = month
        self.day = day
        self.calculated_at = timezone.now()
        self.no_of_queries = Query.objects.filter(
            timestamp__gte=today_midnight, timestamp__lt=tomorrow_midnight
        ).count()
        self.no_of_clients = (
            Query.objects.filter(timestamp__gte=today_midnight, timestamp__lt=tomorrow_midnight)
            .distinct('client')
            .count()
        )
        self.no_of_verified = Query.objects.filter(
            timestamp__gte=today_midnight, timestamp__lt=tomorrow_midnight, was_verified=True
        ).count()
        self.no_of_plScore = Query.objects.filter(
            timestamp__gte=today_midnight, timestamp__lt=tomorrow_midnight, was_plScore=True
        ).count()
        self.no_of_590 = Query.objects.filter(
            timestamp__gte=today_midnight, timestamp__lt=tomorrow_midnight, was_590=True
        ).count()
        self.no_of_not_verified_590 = Query.objects.filter(
            timestamp__gte=today_midnight, timestamp__lt=tomorrow_midnight, was_verified=False, was_590=True
        ).count()
        self.no_of_not_verified_not_590 = Query.objects.filter(
            timestamp__gte=today_midnight, timestamp__lt=tomorrow_midnight, was_verified=False, was_590=False
        ).count()
        self.no_of_new_companies = (
            Company.objects.filter(created__gte=today_midnight, created__lt=tomorrow_midnight)
            .order_by('id')
            .distinct('id')
            .count()
        )
        self.no_of_new_products = (
            Product.objects.filter(created__gte=today_midnight, created__lt=tomorrow_midnight)
            .order_by('id')
            .distinct('id')
            .count()
        )
        self.no_of_new_reports = (
            Report.objects.filter(created__gte=today_midnight, created__lt=tomorrow_midnight)
            .order_by('id')
            .distinct('id')
            .count()
        )


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk and self.__class__.objects.exists():
            raise Exception(f"You can't create more than one instance of {self.__class__.__name__} objects.")
        return super().save(*args, **kwargs)


DEFAULT_DONATE_URL = "https://www.pola-app.pl/1-5-podatku-na-aplikacje-pola"
DEFAULT_DONATE_TEXT = "1,5% podatku na aplikację Pola?"


class AppConfiguration(SingletonModel):
    donate_url = models.URLField(max_length=100, verbose_name="URL Donacji", default=DEFAULT_DONATE_URL)
    donate_text = models.CharField(max_length=255, verbose_name="Tekst Donacji", default=DEFAULT_DONATE_TEXT)

    class Meta:
        verbose_name = 'Konfiguracja aplikacji'

    def __str__(self):
        return "Konfiguracja aplikacji"

    def get_absolute_url(self):
        return reverse('app-config')

    @staticmethod
    def get_singleton():
        app_config = AppConfiguration.objects.first()
        if not app_config:
            app_config = AppConfiguration()
            app_config.save()
        return app_config
