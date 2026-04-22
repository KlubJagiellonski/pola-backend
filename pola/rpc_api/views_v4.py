import json

from django.core.paginator import InvalidPage
from django.db.models import Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit

from pola import logic, logic_ai
from pola.models import AppConfiguration, Query, SearchQuery
from pola.product.models import Product
from pola.rpc_api.api_models import SearchResult, SearchResultCollection
from pola.rpc_api.auth import require_static_bearer_token
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
        if product.company:
            product.company.increment_query_count()

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


@csrf_exempt
@ratelimit(key='ip', rate=whitelist('2/s'), block=True)
def set_product_ingredients_v4(request):
    """Set Product.ingredients by product code.

    Accepts POST with JSON body: {"code": "<ean>", "ingredients": "PL|NPL|<other>"}
    - When value is "PL" or "NPL", store that value.
    - Any other value (including missing) sets the field to null ("Brak danych").
    Returns updated state: {"code": ..., "ingredients": <value or null>}.
    """
    unauthorized = require_static_bearer_token(request)
    if unauthorized is not None:
        return unauthorized

    if request.method != 'POST':
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8")) if request.body else {}
    except Exception:
        return JsonResponse({"detail": "Invalid JSON"}, status=400)

    code = data.get('code') or request.GET.get('code')
    value = data.get('ingredients') or request.GET.get('ingredients')
    if not code:
        return JsonResponse({"detail": "Missing 'code'"}, status=400)

    try:
        product = Product.objects.get(code=code)
    except Product.DoesNotExist:
        return JsonResponse({"detail": "Product not found"}, status=404)

    normalized = (value or '').strip().upper()
    if normalized in {'PL', 'NPL'}:
        product.ingredients = normalized
    else:
        product.ingredients = None

    product.save()

    return JsonResponse(
        {
            "code": product.code,
            "ingredients": product.ingredients,
        }
    )
