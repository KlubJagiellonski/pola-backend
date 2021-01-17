from django.core.management.base import BaseCommand
from django.db import connection

from pola.slack import send_ai_pics_stats

STATEMENT_A = """
SELECT sum(query_count),
       sum(query_count*enough_ai_pics)
FROM
  (SELECT count(DISTINCT pola_query.id) AS query_count,
          CASE
              WHEN count(DISTINCT ai_pics_aiattachment.id)>%s THEN 1
              ELSE 0
          END AS enough_ai_pics
   FROM product_product
   JOIN pola_query ON product_product.id=pola_query.product_id
   LEFT OUTER JOIN ai_pics_aipics ON product_product.id = ai_pics_aipics.product_id
   LEFT OUTER JOIN ai_pics_aiattachment ON ai_pics_aipics.id = ai_pics_id
   WHERE pola_query.timestamp > CURRENT_TIMESTAMP - interval '1 day'
   GROUP BY product_product.id,
            product_product.name) AS sub
"""


class Command(BaseCommand):
    help = 'Sends AI Pics stats to Slack'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute(
                "select count(*) as c0, count(distinct ai_pics_aipics.id) as c1, count(distinct product_id) as c2 "
                "from ai_pics_aipics "
                "join ai_pics_aiattachment on ai_pics_aipics.id = ai_pics_id "
                "where ai_pics_aipics.created_at > current_timestamp - interval '1 day' "
            )
            row = cursor.fetchone()
            msg = 'W ciągu ostatniej doby użytkownicy Poli przysłali {} zdjęć w {} sesjach dla {} produktów.'.format(
                row[0], row[1], row[2]
            )
            send_ai_pics_stats(msg)

            # TODO: Fix tests and statement
            # for i in range(0, 40, 10):
            #     cursor.execute(STATEMENT_A, [i])
            #     row = cursor.fetchone()
            #
            #     msg = (
            #         "W ciągu ostatniej doby użytkownicy Poli zeskanowali produkty {} razy. "
            #         "Mamy więcej niż {} zdjęć AI dla {} "
            #         "zeskanowań, co daje {:.2f}%".format(row[0], i, row[1], 100 * row[1] / row[0])
            #     )
            #     # print msg.encode("utf-8")
            #     send_ai_pics_stats(msg)
