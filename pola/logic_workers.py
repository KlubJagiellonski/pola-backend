# -*- coding: utf-8 -*-

from product.models import Product
from pola.logic import create_from_api
from django.conf import settings
from produkty_w_sieci_api import Client
from django.utils import timezone
from datetime import timedelta
from django_rq import job
from redis import Redis
from rq_scheduler import Scheduler


REQUERY_590_FREQUENCY = 7
REQUERY_590_LIMIT = 10
REQUERY_ALL_FREQUENCY = 30
REQUERY_ALL_LIMIT = 10

# usage:
# python manage.py shell
# from pola.logic_workers import requery_590_codes
# requery_590_codes()

#update product_product set ilim_queried_at='2015/11/11'

#requery products without company, 590-codes, last queried more then 7 days ago
def requery_590_codes():

    p590 = Product.objects\
        .filter(company__isnull=True, code__startswith='590',
                ilim_queried_at__lt=
                timezone.now()-timedelta(days=REQUERY_590_FREQUENCY))\
                [:REQUERY_590_LIMIT]

    requery_products(p590)

@job
def requery_all_codes():
    products = Product.objects\
        .filter(ilim_queried_at__lt=
                timezone.now()-timedelta(days=REQUERY_ALL_FREQUENCY))\
                [:REQUERY_ALL_LIMIT]

#    products = Product.objects.filter(code='5901886015148')

    requery_products(products)

@job
def requery_products(products):
    client = Client(settings.PRODUKTY_W_SIECI_API_KEY)

    for prod in products:
        print prod.code + " -> ",

        if prod.code.isdigit() and\
            (len(prod.code) == 8 or len(prod.code) == 13):
            product_info = client.get_product_by_gtin(prod.code)

        prod.ilim_queried_at = timezone.now()
        prod.save()

        p = create_from_api(prod.code, product_info, product=prod)

        if p.company and p.company.name:
            print p.company.name.encode('utf-8')
        else:
            print "."


scheduler = Scheduler(connection=Redis())

#schedule tasks
scheduler.schedule(
    scheduled_time=datetime.utcnow(), # Time for first execution, in UTC timezone
    func=requery_products,                     # Function to be queued
    interval=120,                   # Time before the function is called again, in seconds
    repeat=None                      # Repeat this number of times (None means repeat forever)
)

scheduler.schedule(
    scheduled_time=datetime.utcnow()
        +timedelta(minutes=1), # Time for first execution, in UTC timezone
    func=requery_590_codes,    # Function to be queued
    interval=120,              # Time before the function is called again, in seconds
    repeat=None                # Repeat this number of times (None means repeat forever)
)
