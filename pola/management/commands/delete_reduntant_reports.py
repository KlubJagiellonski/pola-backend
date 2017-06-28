from django.core.management.base import BaseCommand, CommandError
from product.models import Product
from report.models import Report
from django.db import connection

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

            print "{} (id:{})".format(product['name'].encode('UTF-8') if product['name'] else '', product['id'])

            reports = Report.objects\
                .filter(pk=product['id'], client='krs-bot')\
                .values('id','description')\
                .order_by('created_at')

            desc = []
            for report in reports:

                if report['description'] in desc:
                    print report['description'] + ' - deleted'
                    report.delete()
                else:
                    print report['description']
                    desc.insert(report['description'])

            break
