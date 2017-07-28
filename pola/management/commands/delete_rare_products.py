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
        parser.add_argument('limit')

    def handle(self, *args, **options):
        with connection.cursor() as c:
            c.execute(
                "SELECT id "
                "FROM product_product "
                "WHERE company_id IS NULL AND name IS NULL "
                "AND (select count(*) from report_report where product_id=product_product.id)=0 "
                "AND (select count(*) from pola_query where product_id=product_product.id) < "
                "(12*date_part('year',age(created_at))+ date_part('month',age(created_at))) limit %s",
                [options["limit"]]
            )
            while True:
                row = c.fetchone()
                if not row:
                    return

                product_id = row[0]
#                print product_id
                sys.stdout.write('.')
                sys.stdout.flush()
#                return

                versions = Version.objects.\
                    filter(object_id_int=product_id,
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
                    cursor.execute(
                        'delete from pola_query where product_id=%s',
                        [product_id])
                    cursor.execute(
                        'delete from product_product where id=%s',
                        [product_id])
