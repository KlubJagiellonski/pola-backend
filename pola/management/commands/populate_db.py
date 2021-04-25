from django.core.management import BaseCommand
from django.db import IntegrityError

from company.factories import CompanyFactory
from company.models import Company
from product.factories import ProductFactory
from product.models import Product
from report.factories import (
    AttachmentFactory,
    ReportFactory,
    ResolvedReportFactory,
)
from report.models import Report


class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Delete the database data',
        )

    def handle(self, *args, **options):
        if options['delete']:
            Company.objects.all().delete()
            Product.objects.all().delete()
            Report.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Successfully emptied the database'))
        else:
            try:
                for i in range(5):
                    CompanyFactory.create()
                    ProductFactory.create()
                    ReportFactory.create()
                    ResolvedReportFactory.create()
                    AttachmentFactory.create()
                product = Product.objects.first()
                for i in range(3):
                    ReportFactory.create(product=product, description=f"zgłoszenie {i} z tym samym produktem")
                self.stdout.write(self.style.SUCCESS(f"Product with multiple reports: {product.name}"))
                product = Product.objects.last()
                ReportFactory.create(
                    product=product,
                    client="krs-bot",
                    description="Wg. najnowszego odpytania w bazie ILiM nazwa tego produktu to: test",
                )
                ReportFactory.create(product=product)
                self.stdout.write(self.style.SUCCESS(f"Product with user and bot report: {product.name}"))
                self.stdout.write(self.style.SUCCESS('Successfully populated the database'))
            except IntegrityError:
                self.stdout.write(
                    self.style.ERROR('The database is not empty. To delete the data, use the --delete argument.')
                )
