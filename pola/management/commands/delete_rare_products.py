from django.core.management.base import BaseCommand, CommandError
from product.models import Product
from report.models import Report
from reversion.models import Version
from pola.models import Query
from django.db import connection
from datetime import datetime
import sys

class Command(BaseCommand):
    help = 'Deletes rarely queried products (probably spam)'

    def add_arguments(self, parser):
        parser.add_argument('last_product_id')

    def handle(self, *args, **options):
        i=0;
        products = Product.objects.filter(pk__gte=options["last_product_id"],
                                          company__isnull=True,
                                          name__isnull=True)\
            .order_by('id')[:100000].iterator()
        for product in products:
            if i%100 == 0:
                print
                print product.id
            i+=1

            no_of_reports = Report.objects.filter(product=product).count()
            no_of_queries = Query.objects.filter(product=product).count()

            now = datetime.now()
            age_in_months = (now.year-product.created_at.year)*12 + (now.month-product.created_at.month)

            # delete if product queried less than once per month
            if no_of_reports==0 and no_of_queries < age_in_months:
                sys.stdout.write('.')
                sys.stdout.flush()

                versions = Version.objects.\
                    filter(object_id_int=product.id,
                           content_type_id=15)\
                    .values('id','revision_id').iterator()
                with connection.cursor() as cursor:
                    for version in versions:
                        cursor.execute(
                            'delete from reversion_version where id=%s',
                            [version['id']])
                        cursor.execute(
                            'delete from reversion_revision where id=%s',
                            [version['revision_id']])
                product.delete()
            else:
                sys.stdout.write('o')
                sys.stdout.flush()
