from collections.abc import Iterable
from datetime import timedelta

from django.utils import timezone

from pola.integrations.produkty_w_sieci import produkty_w_sieci_client
from pola.logic_produkty_w_sieci import create_from_api, is_code_supported
from pola.product.models import Product

REQUERY_590_FREQUENCY_DAYS = 30
REQUERY_590_LIMIT = 10000
REQUERY_ALL_FREQUENCY_DAYS = 60
REQUERY_ALL_LIMIT = 10000


def requery_590_codes():
    print("Starting requering 590 codes...")

    p590 = Product.objects.filter(
        company__isnull=True,
        # Check if 590 only is supported by GS1
        code__startswith='590',
        ilim_queried_at__lt=timezone.now() - timedelta(days=REQUERY_590_FREQUENCY_DAYS),
    ).order_by('-query_count')[:REQUERY_590_LIMIT]

    requery_products(p590)

    print("Finished requering 590 codes...")


def requery_all_codes():
    print("Starting requering all codes...")

    products = Product.objects.filter(
        ilim_queried_at__lt=timezone.now() - timedelta(days=REQUERY_ALL_FREQUENCY_DAYS),
    ).order_by('-query_count')[:REQUERY_ALL_LIMIT]

    requery_products(products)

    print("Finished requering all codes...")


def requery_products(products: Iterable[Product]):
    for prod in products:
        print(prod.code, prod.query_count, " -> ")

        prod.ilim_queried_at = timezone.now()
        prod.save()

        try:
            if is_code_supported(prod.code):
                products_response = produkty_w_sieci_client.get_products(gtin_number=prod.code)
                p = create_from_api(prod.code, products_response, product=prod)
                if p and p.company and p.company.name:
                    print(p.company.name.encode(), p.brand)
                else:
                    print(".")
            else:
                print(";")
        except ConnectionError as e:
            print(e)
            raise e
