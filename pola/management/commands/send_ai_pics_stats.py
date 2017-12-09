# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from slack import send_ai_pics_stats

class Command(BaseCommand):
    help = 'Sends AI Pics stats to Slack'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            for i in range(10,40,10):
                cursor.execute(""
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

                msg = u"W ciągu ostatniej doby użytkownicy Poli zeskanowali produkty {} razy. Mamy więcej niż {} zdjęć AI dla {} " \
                      u"zeskanowań, co daje {:.2f}%".format(row[0],i,row[1],100*row[1]/row[0])
                #print msg.encode("utf-8")
                send_ai_pics_stats(msg)
