from django.http import JsonResponse
from ratelimit.decorators import ratelimit

from pola import logic, logic_ai
from pola.models import Query
from pola.rpc_api.openapi import validate_pola_openapi_spec
from pola.rpc_api.rates import whitelist


@ratelimit(key='ip', rate=whitelist('2/s'), block=True)
@validate_pola_openapi_spec
def get_by_code_v4(request):
    noai = request.GET.get('noai')
    result = get_by_code_internal(
        request, ai_supported=noai is None, multiple_company_supported=True, report_as_object=True
    )

    response = JsonResponse(result)
    response["Access-Control-Allow-Origin"] = "*"

    return response


def get_by_code_internal(request, ai_supported=False, multiple_company_supported=False, report_as_object=False):
    code = request.GET['code']
    device_id = request.GET['device_id']

    result, stats, product = logic.get_result_from_code(
        code, multiple_company_supported=multiple_company_supported, report_as_object=report_as_object
    )

    if product is not None:
        Query.objects.create(
            client=device_id,
            product=product,
            was_verified=stats['was_verified'],
            was_590=stats['was_590'],
            was_plScore=stats['was_plScore'],
        )

    if product:
        product.increment_query_count()
        companies = list(product.companies.all())
        if companies:
            for company in companies:
                company.increment_query_count()

    if ai_supported:
        result = logic_ai.add_ask_for_pics(product, result)

    result["donate"] = {
        "show_button": True,
        "url": "https://klubjagiellonski.pl/zbiorka/wspieraj-aplikacje-pola/",
        "title": "Potrzebujemy 1 zł",
    }
    return result
