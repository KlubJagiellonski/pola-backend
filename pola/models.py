from datetime import datetime, timedelta

from django.contrib.postgres.indexes import BrinIndex
from django.db import models
from django.utils import timezone
from django.utils.timezone import get_default_timezone

from company.models import Company
from product.models import Product
from report.models import Report


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
            Company.objects.filter(created_at__gte=today_midnight, created_at__lt=tomorrow_midnight)
            .order_by('id')
            .distinct('id')
            .count()
        )
        self.no_of_new_products = (
            Product.objects.filter(created_at__gte=today_midnight, created_at__lt=tomorrow_midnight)
            .order_by('id')
            .distinct('id')
            .count()
        )
        self.no_of_new_reports = (
            Report.objects.filter(created_at__gte=today_midnight, created_at__lt=tomorrow_midnight)
            .order_by('id')
            .distinct('id')
            .count()
        )
