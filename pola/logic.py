import sentry_sdk

from pola.company.models import Brand
from pola.countries import get_registration_country
from pola.integrations.produkty_w_sieci import (
    ApiException,
    produkty_w_sieci_client,
)
from pola.logic_produkty_w_sieci import create_from_api, is_code_supported
from pola.product.models import Product
from pola.text_utils import strip_urls_newlines

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
            handle_unknown_company(code, report, result)
        elif multiple_company_supported:
            handle_multiple_companies(code, companies, result, stats)
        else:
            handle_companies_when_multiple_companies_are_not_supported(
                code, companies, multiple_company_supported, result, stats
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


def handle_companies_when_multiple_companies_are_not_supported(
    code, companies, multiple_company_supported, result, stats
):
    company = companies[0]
    company_data = serialize_company(company)
    append_ru_by_warning_to_description(code, company_data)
    append_brands_if_enabled(company, company_data)
    stats['was_plScore'] = bool(get_plScore(company))

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


def handle_multiple_companies(code, companies, result, stats):
    companies_data = []

    for company in companies:
        company_data = serialize_company(company)
        append_ru_by_warning_to_description(code, company_data)
        append_brands_if_enabled(company, company_data)
        stats['was_plScore'] = all(get_plScore(c) for c in companies)
        companies_data.append(company_data)
    if len(companies) > 1:
        result['name'] = "Marka własna - Sieć Lidl"
    result['companies'] = companies_data


def handle_unknown_company(code, report, result):
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
                result['plScore'] = 0
                result['card_type'] = TYPE_GREY
                result['name'] = f'Miejsce rejestracji: {registration_country}'
                result['altText'] = (
                    f'Ten produkt został wyprodukowany przez zagraniczną firmę, '
                    f'której miejscem rejestracji jest: {registration_country}. \n'
                    f'Ten kraj dokonał inwazji na Ukrainę. Zastanów się, czy chcesz go kupić.'
                )
            else:
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
    plScore = get_plScore(company)
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
            if is_code_supported(code):
                products_response = produkty_w_sieci_client.get_products(gtin_number__prefix=f"0{code}")

                return create_from_api(code, products_response, product=None)
        except ApiException as ex:
            sentry_sdk.capture_exception(ex)
    return Product.objects.create(code=code)


def get_plScore(company):
    if (
        company.plCapital is not None
        and company.plWorkers is not None
        and company.plRnD is not None
        and company.plRegistered is not None
        and company.plNotGlobEnt is not None
    ):
        return int(
            0.35 * company.plCapital
            + 0.30 * company.plWorkers
            + 0.15 * company.plRnD
            + 0.10 * company.plRegistered
            + 0.10 * company.plNotGlobEnt
        )
    else:
        return None
