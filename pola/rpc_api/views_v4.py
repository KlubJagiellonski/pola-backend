from django.core.paginator import InvalidPage
from django.db import connection
from django.db.models import Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django_ratelimit.decorators import ratelimit

from pola import logic, logic_ai
from pola.models import AppConfiguration, Query, SearchQuery
from pola.product.models import Product
from pola.rpc_api.api_models import SearchResult, SearchResultCollection
from pola.rpc_api.http import JsonProblemResponse
from pola.rpc_api.openapi import validate_pola_openapi_spec
from pola.rpc_api.paginator import TokenizedPaginator
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


def _extract_barcode_from_query_source(query_source: str) -> str | None:
    if query_source and query_source.startswith('alt_'):
        return query_source[4:]
    return None


def _increment_replacements_query_count(barcode_from: str, barcode_to: str):
    "Increment counters for recorded replacement selection"
    with connection.cursor() as cursor:
        cursor.execute(
            (
                "UPDATE product_product_replacements r "
                "SET counts = r.counts + 1 "
                "FROM product_product pfrom, product_product pto "
                "WHERE r.from_product_id = pfrom.id "
                "AND r.to_product_id = pto.id "
                "AND pfrom.code = %s "
                "AND pto.code = %s"
            ),
            [barcode_from, barcode_to],
        )


def get_by_code_internal(request, ai_supported=False, multiple_company_supported=False, report_as_object=False):
    code = request.GET['code']
    device_id = request.GET['device_id']
    query_source = request.GET.get('query_source', 'scanner')

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

    if product and query_source == 'scanner':
        product.increment_query_count()
        if product.company:
            product.company.increment_query_count()
    if query_source and query_source.startswith('alt_'):
        barcode_from = _extract_barcode_from_query_source(query_source)
        barcode_to = product.code if product else None
        if barcode_from and barcode_to and barcode_from != barcode_to:
            _increment_replacements_query_count(barcode_from, barcode_to)

    if ai_supported:
        result = logic_ai.add_ask_for_pics(product, result)

    app_configuration = AppConfiguration.get_singleton()
    result["donate"] = {
        "show_button": True,
        "title": app_configuration.donate_text,
        "url": app_configuration.donate_url,
    }
    return result


class SearchV4ApiView(View):
    PAGE_SIZE = 10

    @method_decorator(ratelimit(key='ip', rate=whitelist('2/s'), block=True))
    @method_decorator(validate_pola_openapi_spec)
    def get(self, request):
        query = request.GET['query']
        qs = self.get_queryset(query)
        paginator = TokenizedPaginator(qs.all(), self.PAGE_SIZE, token_salt=self.__class__.__name__)
        page_token = request.GET.get('pageToken')
        if page_token is None:
            SearchQuery(client=request.GET.get('device_id'), text=query).save()
        try:
            page = paginator.get_page_by_token(page_token)
        except InvalidPage as e:
            return JsonProblemResponse(status=400, title="Invalid value of pageToken parameter", detail=str(e))

        return JsonResponse(
            SearchResultCollection(
                nextPageToken=page.next_page_token() if page.has_next() else None,
                products=[SearchResult.create_from_product(p) for p in page],
                totalItems=paginator.count,
            )
        )

    def get_queryset(self, query):
        pred = Q(name__icontains=query)
        if len(query) in (13, 9) and query.isnumeric():
            pred = pred | Q(code=query)
        qs = Product.objects.filter(pred).order_by('pk')
        return qs
