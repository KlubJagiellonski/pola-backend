from django.core.management.base import BaseCommand
from django.db import connection
from slack import send_ai_pics_stats


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
            msg = 'W ciągu ostatniej doby użytkownicy Poli przysłali {} zdjęć w {} sesjach dla {} produktów.' \
                .format(row[0], row[1], row[2])
            send_ai_pics_stats(msg)

            for i in range(0, 40, 10):
                cursor.execute(
                    "select sum(query_count), sum(query_count*enough_ai_pics) from "
                    "("
                    "select count(distinct pola_query.id) as query_count, "
                    "case when count(distinct ai_pics_aiattachment.id)>%s then 1 else 0 end as enough_ai_pics "
                    "from product_product "
                    "join pola_query on product_product.id=pola_query.product_id "
                    "left outer join ai_pics_aipics on product_product.id = ai_pics_aipics.product_id "
                    "left outer join ai_pics_aiattachment on ai_pics_aipics.id = ai_pics_id "
                    "where pola_query.timestamp > current_timestamp - interval '1 day' "
                    "group by product_product.id, product_product.name "
                    ") as sub", [i]
                )
                row = cursor.fetchone()

                msg = u"W ciągu ostatniej doby użytkownicy Poli zeskanowali produkty {} razy. " \
                      u"Mamy więcej niż {} zdjęć AI dla {} " \
                      u"zeskanowań, co daje {:.2f}%".format(row[0], i, row[1], 100 * row[1] / row[0])
                # print msg.encode("utf-8")
                send_ai_pics_stats(msg)
