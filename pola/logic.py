import sentry_sdk
from django.conf import settings

from pola.company.models import Brand
from pola.countries import get_registration_country
from pola.integrations.produkty_w_sieci import (
    ApiException,
    produkty_w_sieci_client,
)
from pola.logic_produkty_w_sieci import create_from_api, is_code_supported
from pola.logic_score import get_pl_score
from pola.product.models import Product
from pola.text_utils import _shorten_txt, strip_urls_newlines

WAR_COUNTRIES = ('Federacja Rosyjska', "Białoruś")

TYPE_RED = 'type_red'
TYPE_WHITE = 'type_white'
TYPE_GREY = 'type_grey'

DEFAULT_COMPANY_DATA = {
    'name': None,
    'plCapital': None,
    'plCapital_notes': None,
    'plWorkers': None,
    'plWorkers_notes': None,
    'plRnD': None,
    'plRnD_notes': None,
    'plRegistered': None,
    'plRegistered_notes': None,
    'plNotGlobEnt': None,
    'plNotGlobEnt_notes': None,
    'plScore': None,
    'official_url': None,
    'logotype_url': None,
}

DEFAULT_REPORT_DATA = {
    'text': 'Zgłoś jeśli posiadasz bardziej aktualne dane na temat tego produktu',
    'button_text': 'Zgłoś',
    'button_type': TYPE_WHITE,
}

DEFAULT_RESULT = {
    'product_id': None,
    'code': None,
    'name': None,
    'card_type': TYPE_WHITE,
    'altText': None,
}

DEFAULT_STATS = {'was_verified': False, 'was_590': False, 'was_plScore': False}


def get_result_from_code(code, multiple_company_supported=False, report_as_object=False):
    result = DEFAULT_RESULT.copy()
    stats = DEFAULT_STATS.copy()
    report = DEFAULT_REPORT_DATA.copy()
    product = None

    result['code'] = code
    if not multiple_company_supported:
        result.update(DEFAULT_COMPANY_DATA)
    if code.isdigit() and (len(code) == 8 or len(code) == 13):
        # code is EAN8 or EAN13
        product = get_by_code(code)
        if product:
            product_company = product.company
            brand_company = product.brand.company if product.brand else None
            companies = []
            if product_company:
                companies.append(product_company)
                result['name'] = product_company.common_name or product_company.official_name or product_company.name
            if brand_company:
                companies.append(brand_company)
            companies = list(({c.pk: c for c in companies}).values())
            result['product_id'] = product.id
            stats['was_590'] = code.startswith('590')
            if not product_company:
                handle_unknown_company(code, report, result, multiple_company_supported)
            elif multiple_company_supported:
                handle_multiple_companies(code, companies, result, stats, product_company)
            else:
                handle_companies_when_multiple_companies_are_not_supported(
                    code, companies, multiple_company_supported, result, stats
                )
            handle_product_replacements(product, result, report)
        else:
            result['name'] = 'Nieznany produkt'
            result['altText'] = (
                'Produkt nie został znaleziony w bazie i nie udało się go automatycznie utworzyć '
                'na bazie danych zewnętrznych.'
            )
    else:
        # not an EAN8 nor EAN13 code. Probably QR code or some error
        result['name'] = 'Nieprawidłowy kod'
        result['altText'] = (
            'Pola rozpoznaje tylko kody kreskowe typu EAN8 i '
            'EAN13. Zeskanowany przez Ciebie kod jest innego '
            'typu. Spróbuj zeskanować kod z czegoś innego'
        )
    if report_as_object:
        result['report'] = report
    else:
        result.update({("report_" + k, v) for k, v in report.items()})
    return result, stats, product


def serialize_brand(brand):
    logotype_url = brand.logotype.url if brand.logotype else None
    website_url = brand.website_url if brand.website_url else None
    return {'name': str(brand), 'logotype_url': logotype_url, 'website_url': website_url}


def _find_replacements(replacements_rel):
    """Find replacements for a product and serialize them."""
    items = []
    for r in replacements_rel.order_by("id"):
        company = r.company
        company_name = None
        if company:
            company_name = company.common_name or company.official_name or company.name
        brand_name = None
        if getattr(r, "brand", None):
            brand_name = r.brand.common_name or r.brand.name
        prod_name = r.name or r.code
        if not prod_name:
            continue
        # Prefer brand name when available; otherwise fall back to a company name
        chosen_name = brand_name or company_name
        display_name = f"{_shorten_txt(prod_name, 40)} ({_shorten_txt(chosen_name, 30)})" if chosen_name else prod_name
        items.append(
            {
                "code": r.code,
                "name": prod_name,
                "company": chosen_name,
                "description": company.description if company else None,
                "display_name": display_name,
                "is_friend": bool(company.is_friend) if company else False,
            }
        )
    return items


def handle_product_replacements(product, result, report, topK=3):
    """If the product has replacements, add them to the result and modify the report text.

    Args:
        product: Product instance
        result: results dict to be modified
        report: report dict to be modified
        topK: maximum number of replacements to include in the report text
    """
    replacements = _find_replacements(product.replacements)
    if replacements:
        result["replacements"] = replacements
        if report['text']:
            report_text = report['text']
            txt_replacements = ', '.join(f"{r['display_name']}" for r in replacements[:topK])
            report['text'] = f"Polskie alternatywy: {txt_replacements}" f"\n---\n{report_text}"


def handle_companies_when_multiple_companies_are_not_supported(
    code, companies, multiple_company_supported, result, stats
):
    company = companies[0]
    company_data = serialize_company(company)
    append_ru_by_warning_to_description(code, company_data)
    append_brands_if_enabled(company, company_data)
    stats['was_plScore'] = bool(get_pl_score(company))

    result.update(company_data)
    stats['was_verified'] = company.verified
    result['card_type'] = TYPE_WHITE if company.verified else TYPE_GREY


def append_ru_by_warning_to_description(code, company_data):
    registration_country = get_registration_country(code)
    if registration_country not in WAR_COUNTRIES:
        return

    if company_data['description']:
        company_data['description'] += "\n"

    company_data['description'] += (
        f'Ten produkt został wyprodukowany przez zagraniczną firmę, '
        f'której miejscem rejestracji jest: {registration_country}. \n'
        f'Ten kraj dokonał inwazji na Ukrainę. Zastanów się, czy chcesz go kupić.'
    )


def append_brands_if_enabled(company, company_data):
    if not company.display_brands_in_description:
        return
    if company_data['description']:
        company_data['description'] += "\n"

    brand_list = ", ".join(sorted(str(brand) for brand in Brand.objects.filter(company=company)))
    company_data['description'] += f'Ten producent psoiada marki: {brand_list}.'


def add_brands(company_data, product_company):
    if product_company:
        company_data['brands'] = [serialize_brand(brand) for brand in Brand.objects.filter(company=product_company)]


def handle_multiple_companies(code, companies, result, stats, product_company):
    companies_data = []

    for company in companies:
        company_data = serialize_company(company)
        append_ru_by_warning_to_description(code, company_data)
        append_brands_if_enabled(company, company_data)
        add_brands(company_data, product_company)
        stats['was_plScore'] = all(get_pl_score(c) for c in companies)
        companies_data.append(company_data)
    result['companies'] = companies_data


def handle_unknown_company(code, report, result, multiple_company_supported):
    # we don't know the manufacturer
    if code.startswith('590'):
        # the code is registered in Poland, we want more data!
        result['name'] = "Tego produktu nie mamy jeszcze w bazie"
        result['altText'] = (
            "Każde skanowanie jest rejestrowane. Najczęściej skanowane firmy i produkty, "
            "których nie mamy jeszcze w bazie, są weryfikowane w pierwszej kolejności. "
            "Nie pobieramy przy tym żadnych informacji o użytkowniku.\n"
            "\n"
            "Jeśli chcesz zgłosić błąd lub wyrazić opinię, prosimy o kontakt: pola@klubjagiellonski.pl"
        )
        result['card_type'] = TYPE_GREY
        report['text'] = "Bardzo prosimy o zgłoszenie nam tego produktu"
        report['button_type'] = TYPE_RED
    elif code.startswith('977') or code.startswith('978') or code.startswith('979'):
        # this is an ISBN/ISSN/ISMN number
        # (book, music album or magazine)
        result['name'] = 'Kod ISBN/ISSN/ISMN'
        result['altText'] = (
            'Zeskanowany kod jest kodem '
            'ISBN/ISSN/ISMN dotyczącym książki,  '
            'czasopisma lub albumu muzycznego. '
            'Wydawnictwa tego typu nie są aktualnie '
            'w obszarze zainteresowań Poli.'
        )
        report['text'] = "To nie jest książka, czasopismo lub album muzyczny? Prosimy o zgłoszenie"
    else:
        registration_country = get_registration_country(code)

        if registration_country:
            if registration_country in ('Federacja Rosyjska', "Białoruś"):
                if not multiple_company_supported:
                    result['plScore'] = 0
                result['card_type'] = TYPE_GREY
                result['name'] = f'Miejsce rejestracji: {registration_country}'
                result['altText'] = (
                    f'Ten produkt został wyprodukowany przez zagraniczną firmę, '
                    f'której miejscem rejestracji jest: {registration_country}. \n'
                    f'Ten kraj dokonał inwazji na Ukrainę. Zastanów się, czy chcesz go kupić.'
                )
            else:
                if not multiple_company_supported:
                    result['plScore'] = 0
                result['card_type'] = TYPE_GREY
                result['name'] = f'Miejsce rejestracji: {registration_country}'
                result['altText'] = (
                    f'Ten produkt został wyprodukowany przez zagraniczną firmę, '
                    f'której miejscem rejestracji jest: {registration_country}.'
                )
        else:
            # Ups. It seems to be an internal code
            result['name'] = 'Kod wewnętrzny'
            result['altText'] = (
                'Zeskanowany kod jest wewnętrznym '
                'kodem sieci handlowej. Pola nie '
                'potrafi powiedzieć o nim nic więcej'
            )


def serialize_company(company):
    plScore = get_pl_score(company)
    company_data = DEFAULT_COMPANY_DATA.copy()
    # we know the manufacturer of the product
    company_data['name'] = company.common_name or company.official_name or company.name
    company_data['plCapital'] = company.plCapital
    company_data['plCapital_notes'] = company.plCapital_notes
    company_data['plWorkers'] = company.plWorkers
    company_data['plWorkers_notes'] = company.plWorkers_notes
    company_data['plRnD'] = company.plRnD
    company_data['plRnD_notes'] = company.plRnD_notes
    company_data['plRegistered'] = company.plRegistered
    company_data['plRegistered_notes'] = company.plRegistered_notes
    company_data['plNotGlobEnt'] = company.plNotGlobEnt
    company_data['plNotGlobEnt_notes'] = company.plNotGlobEnt_notes
    company_data['is_friend'] = company.is_friend
    if company.is_friend:
        company_data['friend_text'] = 'To jest przyjaciel Poli'
    if company.description:
        company_data['description'] = company.description
    else:
        desc = ''
        if company.plCapital_notes:
            desc += strip_urls_newlines(company.plCapital_notes) + '\n'
        if company.plWorkers_notes:
            desc += strip_urls_newlines(company.plWorkers_notes) + '\n'
        if company.plRnD_notes:
            desc += strip_urls_newlines(company.plRnD_notes) + '\n'
        if company.plRegistered_notes:
            desc += strip_urls_newlines(company.plRegistered_notes) + '\n'
        if company.plNotGlobEnt_notes:
            desc += strip_urls_newlines(company.plNotGlobEnt_notes) + '\n'

        company_data['description'] = desc
    company_data['sources'] = company.get_sources(raise_exp=False)
    if plScore:
        company_data['plScore'] = plScore
    company_data['official_url'] = company.official_url
    if company.logotype:
        company_data['logotype_url'] = company.logotype.url
    return company_data


def get_by_code(code):
    try:
        return Product.objects.get(code=code)
    except Product.DoesNotExist:
        try:
            if is_code_supported(code) and settings.PRODUKTY_W_SIECI_ENABLE:
                products_response = produkty_w_sieci_client.get_products(gtin_number=code)
                return create_from_api(code, products_response, product=None)
        except ApiException as ex:
            sentry_sdk.capture_exception(ex)
    return Product.objects.create(code=code)
