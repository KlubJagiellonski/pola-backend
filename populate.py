import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'pola.config.settings.local')

import django
django.setup()

from company.models import Company
from product.models import Product
from report.models import Report
from company.factories import CompanyFactory
from report.factories import ReportFactory, ResolvedReportFactory, AttachmentFactory
from product.factories import ProductFactory


def populate():
    Company.objects.all().delete()
    Product.objects.all().delete()
    Report.objects.all().delete()
    for i in range(10):
        CompanyFactory.create()
        ProductFactory.create()
        ReportFactory.create()
        ResolvedReportFactory.create()
        AttachmentFactory.create()
    product = Product.objects.first()
    for i in range(3):
        ReportFactory.create(product=product, description=f"zgłoszenie {i} z tym samym produktem")


if __name__ == '__main__':
    print("Starting population script")
    populate()
    print("Finished")
