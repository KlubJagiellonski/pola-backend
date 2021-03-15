from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils import timezone

from company.models import Company
from pola.logic import create_from_api
from pola.produkty_w_sieci_api import (
    Client,
    ConnectionError,
    is_code_supported_by_gs1_api,
)
from product.models import Product

REQUERY_590_FREQUENCY = 30
REQUERY_590_LIMIT = 10000
REQUERY_ALL_FREQUENCY = 60
REQUERY_ALL_LIMIT = 10000

# usage:
# python manage.py shell
# from pola.logic_workers import requery_590_codes
# requery_590_codes()

# update product_product set ilim_queried_at='2015/11/11'

# requery products without company, 590-codes, last queried more then 7 days ago


def requery_590_codes():
    print("Starting requering 590 codes...")

    p590 = Product.objects.filter(
        company__isnull=True,
        code__startswith='590',
        ilim_queried_at__lt=timezone.now() - timedelta(days=REQUERY_590_FREQUENCY),
    ).order_by('-query_count')[:REQUERY_590_LIMIT]

    #    p590 = products = Product.objects.filter(code='5909990022380')

    requery_products(p590)

    print("Finished requering 590 codes...")


def requery_all_codes():
    print("Starting requering all codes...")

    products = Product.objects.filter(
        #            company__isnull=True,
        ilim_queried_at__lt=timezone.now()
        - timedelta(days=REQUERY_ALL_FREQUENCY)
    ).order_by('-query_count')[:REQUERY_ALL_LIMIT]

    #    products = Product.objects.filter(code='142222157008')

    requery_products(products)

    print("Finished requering all codes...")


def requery_products(products):
    client = Client(settings.PRODUKTY_W_SIECI_API_USERNAME, settings.PRODUKTY_W_SIECI_API_PASSWORD)

    for prod in products:
        print(prod.code, prod.query_count, " -> ")

        prod.ilim_queried_at = timezone.now()
        prod.save()

        try:
            if is_code_supported_by_gs1_api(prod.code):
                product_info = client.get_product_by_gtin(prod.code)

                p = create_from_api(prod.code, product_info, product=prod)

                if p.company and p.company.name:
                    print(p.company.name.encode('utf-8'), p.brand)
                else:
                    print(".")
            else:
                print(";")
        except ConnectionError as e:
            print(e)


def update_company_from_krs(prod, company):
    return False


def update_from_kbpoz(db_filename):
    with open(db_filename) as f:
        for line in f:
            split = line.split('\t')
            gtin = split[0].strip()
            if len(gtin) > 13:
                gtin = gtin[1:]

            if len(split) > 1:
                nip = split[1].strip()

                try:
                    prod = Product.objects.get(code=gtin)
                    if not prod.company and nip != "":
                        with transaction.atomic():
                            try:
                                company = Company.objects.get(nip=nip)
                            except ObjectDoesNotExist:
                                company = Company.objects.create(nip=nip)
                                if not update_company_from_krs(prod, company):
                                    company.delete()
                                    continue
                                print("!")

                            print(gtin + " " + nip)
                            print(company)
                            prod.company = company
                            prod.ilim_queried_at = timezone.now()
                            Product.save(
                                prod,
                                commit_desc="Produkt przypisany do producenta na podstawie bazy " "KBPOZ",
                            )

                except ObjectDoesNotExist:
                    pass
