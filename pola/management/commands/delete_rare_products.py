import sys
import textwrap

from django.core.management.base import BaseCommand
from django.db import connection
from reversion.models import Version


class Command(BaseCommand):
    help = 'Deletes rarely queried products (probably spam)'

    def add_arguments(self, parser):
        parser.add_argument('limit')

    def handle(self, *args, **options):
        with connection.cursor() as c:
            i = 0
            c.execute(
                textwrap.dedent(
                    """\
SELECT id
FROM product_product
WHERE 1 = 1
  AND company_id IS NULL
  AND name IS NULL
  AND (SELECT count(*)
       FROM product_product_companies
       WHERE product_id = product_product_companies.id) = 0
  AND (SELECT count(*)
       FROM report_report
       WHERE product_id = product_product.id) = 0
  AND (SELECT count(*)
       FROM ai_pics_aipics
       WHERE product_id = product_product.id) = 0
  AND (SELECT count(*)
       FROM pola_query
       WHERE product_id = product_product.id
      )
      <
      (12 * date_part('year', age(created_at)) + date_part('month', age(created_at)))
LIMIT %s
"""
                ),
                [options["limit"]],
            )
            while True:
                row = c.fetchone()
                if not row:
                    return

                if i % 100 == 0:
                    sys.stdout.write('.')
                    sys.stdout.flush()
                i += 1

                product_id = row[0]
                versions = (
                    Version.objects.filter(object_id=product_id, content_type_id=15)
                    .values('id', 'revision_id')
                    .iterator()
                )
                with connection.cursor() as cursor:
                    for version in versions:
                        cursor.execute('delete from reversion_version where id=%s', [version['id']])
                        cursor.execute('delete from reversion_revision where id=%s', [version['revision_id']])
                    cursor.execute('delete from pola_query where product_id=%s', [product_id])
                    cursor.execute('delete from product_product where id=%s', [product_id])
