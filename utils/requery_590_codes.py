from product.models import Product
from pola.logic import create_from_api
from django.conf import settings
from produkty_w_sieci_api import Client

# usage:
# python manage.py shell
# execfile('utils/requery_590_codes.py')

client = Client(settings.PRODUKTY_W_SIECI_API_KEY)

p590 = Product.objects.with_query_count()\
    .filter(company__isnull=True, code__startswith='590')\
    .order_by('-query_count')

for prod in p590:
    print prod.code

    product_info = client.get_product_by_gtin(prod.code)

    p = create_from_api(prod.code, product_info, product=prod)

    if p.company:
        print p.company.name.encode('utf-8')
    else:
        print "..."

