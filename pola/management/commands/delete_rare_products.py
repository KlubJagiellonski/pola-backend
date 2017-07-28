from django.core.management.base import BaseCommand, CommandError
from product.models import Product
from report.models import Report
from reversion.models import Version
from pola.models import Query
from django.db import connection
from datetime import datetime

class Command(BaseCommand):
    help = 'Deletes rarely queried products (probably spam)'

    def add_arguments(self, parser):
        parser.add_argument('last_product_id')

    def handle(self, *args, **options):
        products = Product.objects.filter(pk__gte=options["last_product_id"])\
            .order_by('id')[:100].iterator()
        for product in products:
            print "{}:{} (id:{})".format(product.code, product.name.encode('utf-8') if product.name else '', product.id)

            no_of_reports = Report.objects.filter(product=product).count()
            no_of_queries = Query.objects.filter(product=product).count()

            print 'Reports: {}, Queries: {}'.format(no_of_reports, no_of_queries)
            now = datetime.now()
            age_in_months = (now.year-product.created_at.year)*12 + (now.month-product.created_at.month)
            print product.created_at
            print age_in_months

            # delete if product queried less than once per month
            if no_of_reports==0 and no_of_queries < age_in_months:
                print 'delete'
                return
                with transaction.atomic():
                    versions = Version.objects.\
                        filter(object_id_int=product.id,
                               content_type_id=15)\
                        .values('id','revision_id')

                    with connection.cursor() as cursor:
                        for version in versions:
                            if record_no>0:
                                cursor.execute(
                                    'delete from reversion_version where id=%s',
                                    [version['id']])
                                cursor.execute(
                                    'delete from reversion_revision where id=%s',
                                    [version['revision_id']])
                    product.delete()
