from sets import Set

from django.core.management.base import BaseCommand

from product.models import Product
from report.models import Report


class Command(BaseCommand):
    help = 'Deletes redundant reports'

    def add_arguments(self, parser):
        parser.add_argument('last_product_id')

    def handle(self, *args, **options):
        print 'Starting...'

        products = Product.objects.filter(pk__gte=options["last_product_id"]) \
            .values('id', 'name') \
            .order_by('id').iterator()

        for product in products:

            print "{} (id:{})".format(product['name'].encode('UTF-8')
                                      if product['name'] else '', product['id'])

            reports = Report.objects\
                .filter(product__id=product['id'], client='krs-bot')\
                .order_by('created_at')

            desc = Set()
            for report in reports:

                if report.description in desc:
                    print report.description.encode('utf-8') + ' - deleted'
                    report.delete()
                else:
                    print report.description.encode('utf-8')
                    desc.add(report.description)
