# -*- coding: utf-8 -*-

from product.models import Product
from company.models import Company
from pola.logic import create_from_api, update_company_from_krs
from django.conf import settings
from produkty_w_sieci_api import Client
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
import pola.UnicodeWriter


# usage:
# python manage.py shell
# from pola.logic_brands import detect_brands
# detect_brands()

def detect_brands():
    print "Starting brands detection..."

    products = Product.objects\
        .filter(
        company__isnull=True,
        code__startswith='590')\
        .order_by('-query_count')

    words={}

    for prod in products:
        for w in prod.name.split():
            word = words.setdefault(w, {'count':0, 'companies':{}})
            word['count'] += 1
            word['companies'].setdefault(prod.company, 0)
            word['companies'][prod.company] += 1

    sorted_words = sorted(words.items(), key=lambda x: x[1]['count'],
                          reverse=True)

    i=0
    k=0
    while k<100:
        if len(sorted_words[i][1]['companies']) <= 1:
            print u'{} - {}, {}'.format(repr(sorted_words[i][0]),
                                    sorted_words[i][1]['count'],
                                    len(sorted_words[i][1]['companies']))
            k+=1
        i+=1

    print "Finished brands detection..."
