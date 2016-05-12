# -*- coding: utf-8 -*-

from company.models import Company
from product.models import Product
from mojepanstwo_api import KrsClient
from produkty_w_sieci_api import Client
import produkty_w_sieci_api
import mojepanstwo_api
from django.conf import settings
import locale
from report.models import Report
import re


def get_result_from_code(code):
    result = DEFAULT_RESULT.copy()
    stats = DEFAULT_STATS.copy()
    product = None

    result['code'] = code

    if code.isdigit() and (len(code) == 8 or len(code) == 13):
        # code is EAN8 or EAN13
        product = get_by_code(code)
        company = product.company

        result['product_id'] = product.id
        stats['was_590'] = code.startswith('590')

        if company:
            # we know the manufacturer of the product
            result['name'] = company.common_name or \
                company.official_name or company.name
            result['plCapital'] = company.plCapital
            result['plCapital_notes'] = company.plCapital_notes
            result['plWorkers'] = company.plWorkers
            result['plWorkers_notes'] = company.plWorkers_notes
            result['plRnD'] = company.plRnD
            result['plRnD_notes'] = company.plRnD_notes
            result['plRegistered'] = company.plRegistered
            result['plRegistered_notes'] = company.plRegistered_notes
            result['plNotGlobEnt'] = company.plNotGlobEnt
            result['plNotGlobEnt_notes'] = company.plNotGlobEnt_notes

            if company.description:
                result['description'] = company.description
            else:
                desc = ''
                if company.plCapital_notes:
                    desc += strip_urls_newlines(company.plCapital_notes)+u'\n'
                if company.plWorkers_notes:
                    desc += strip_urls_newlines(company.plWorkers_notes)+u'\n'
                if company.plRnD_notes:
                    desc += strip_urls_newlines(company.plRnD_notes)+u'\n'
                if company.plRegistered_notes:
                    desc +=\
                        strip_urls_newlines(company.plRegistered_notes)+u'\n'
                if company.plNotGlobEnt_notes:
                    desc +=\
                        strip_urls_newlines(company.plNotGlobEnt_notes)+u'\n'

                result['description'] = desc

            result['sources'] = company.get_sources(raise_exp=False)

            plScore = get_plScore(company)
            if plScore:
                result['plScore'] = plScore
                stats['was_plScore'] = True

            stats['was_verified'] = company.verified
            result['card_type'] = TYPE_WHITE if company.verified else TYPE_GREY

        else:
            # we don't know the manufacturer
            if code.startswith('590'):
                # the code is registered in Poland, we want more data!
                result['name'] = "Zgłoś nam ten kod!"
                result['altText'] = "Zeskanowałeś kod, którego nie mamy " \
                                    "jeszcze w bazie. Bardzo prosimy o " \
                                    "zgłoszenie tego kodu "\
                                    "i wysłania zdjęć zarówno " \
                                    "kodu kreskowego jak i etykiety z " \
                                    "produktu. Z góry dziękujemy!"
                result['report_text'] = "Bardzo prosimy o zgłoszenie nam tego " \
                                        "produktu"
                result['card_type'] = TYPE_GREY
                result['report_button_type'] = TYPE_RED
            elif code.startswith('977') or code.startswith('978') \
                    or code.startswith('979'):
                # this is an ISBN/ISSN/ISMN number
                # (book, music album or magazine)
                result['name'] = 'Kod ISBN/ISSN/ISMN'
                result['altText'] = 'Zeskanowany kod jest kodem ' \
                                    'ISBN/ISSN/ISMN dotyczącym książki,  ' \
                                    'czasopisma lub albumu muzycznego. ' \
                                    'Wydawnictwa tego typu nie są aktualnie ' \
                                    'w obszarze zainteresowań Poli.'
                result['report_text'] = "To nie jest książka, czasopismo lub "\
                                        "album muzyczny? Prosimy o zgłoszenie"
            else:
                # let's try to associate the code with a country
                for prefix in CODE_PREFIX_TO_COUNTRY.keys():
                    if code.startswith(prefix):
                        result['plScore'] = 0
                        result['card_type'] = TYPE_GREY
                        result['name'] = 'Miejsce rejestracji: {}' \
                            .format(CODE_PREFIX_TO_COUNTRY[prefix])
                        result['altText'] = 'Ten produkt został wyprodukowany ' \
                                            'przez zagraniczną firmę, której ' \
                                            'miejscem rejestracji jest: {}.'\
                                        .format(CODE_PREFIX_TO_COUNTRY[prefix])
                        break
                else:
                    # Ups. It seems to be an internal code
                    result['name'] = 'Kod wewnętrzny'
                    result['altText'] = 'Zeskanowany kod jest wewnętrznym ' \
                                        'kodem sieci handlowej. Pola nie ' \
                                        'potrafi powiedzieć o nim nic więcej'

    else:
        # not an EAN8 nor EAN13 code. Probably QR code or some error
        result['name'] = 'Nieprawidłowy kod'
        result['altText'] = 'Pola rozpoznaje tylko kody kreskowe typu EAN8 i '\
                            'EAN13. Zeskanowany przez Ciebie kod jest innego '\
                            'typu. Spróbuj zeskanować kod z czegoś innego'

    return result, stats, product


def get_by_code(code):
    try:
        return Product.objects.get(code=code)
    except Product.DoesNotExist:
        pass
    try:
        client = Client(settings.PRODUKTY_W_SIECI_API_KEY)
        product_info = client.get_product_by_gtin(code)
        return create_from_api(code, product_info)
    except produkty_w_sieci_api.ApiError:
        pass
    return Product.objects.create(code=code)


def create_from_api(code, obj, product=None):
    obj_owner_name = None
    obj_product_name = None

    if obj:
        obj_data = obj.get('Data', {}) or {}
        obj_owner = obj_data.get('Owner', {}) or {}
        obj_owner_name = obj_owner.get('Name', None)
        obj_product = obj_data.get('Product', {}) or {}
        obj_product_name = obj_product.get('Name', None)

    if obj_owner_name:
        company, company_created = Company.objects.get_or_create(
            name=obj_owner_name,
            commit_desc='Firma utworzona automatycznie na podstawie API'
                        ' ILiM')
    else:
        company = None

    if not product:
        product = Product.objects.create(
            name=obj_product_name,
            code=code,
            company=company,
            commit_desc="Produkt utworzony automatycznie na podstawie skanu "
                        "użytkownika")
    else:
        if product.name:
            if obj_product_name and product.name != obj_product_name:
                create_bot_report(product,
                                  u"Wg. najnowszego odpytania w bazie ILiM "
                                  "nazwa tego produktu to:\"{}\"".format(
                                      obj_product_name
                                  ))
        else:
            product.name = obj_product_name

        if product.company:
            if company and product.company.name and obj_owner_name and\
                not ilim_compare_str(product.company.name, obj_owner_name):
                create_bot_report(product,
                                  u"Wg. najnowszego odpytania w bazie ILiM "
                                  "producent tego produktu to:\"{}\"".format(
                                      obj_owner_name
                                  ))
        else:
            product.company = company
        product.save()

    if company and company_created:
        update_company_from_krs(product, company)

    return product


def update_company_from_krs(product, company):
    try:
        krs = KrsClient()
        if company.name:
            companies = krs.get_companies_by_name(company.name)
        elif company.nip:
            companies = krs.get_companies_by_nip(company.nip)
        else:
            return False
        if companies.__len__() == 1:
            company.official_name = companies[0]['nazwa']
            company.common_name = companies[0]['nazwa_skrocona']
            company.address = companies[0]['adres']
            company.nip = companies[0]['nip']
            company.plRegistered = 100
            company.sources = u"Dane z KRS|%s" % companies[0]['url']

            Company.save(company, commit_desc="Dane firmy pobrane "
                                              "automatycznie poprzez API "
                                              "mojepanstwo.pl ({})"
                         .format(companies[0]['url']))

            shareholders = shareholders_to_str(krs, companies[0]['id'], '')
            if shareholders:
                create_bot_report(product, u'Wspólnicy spółki {}:\n{}'.
                                  format(company.name, shareholders))
            return True

        elif companies.__len__() > 0:
            description = u'{} - ta firma może być jedną z następujących:\n\n' \
                .format(company.name)

            for i in range(0, min(companies.__len__(), 10)):
                description += \
                    (u'Nazwa: {}\n' +
                     u'Skrót: {}\n' +
                     u'NIP:   {}\n' +
                     u'Adres: \n{}\n' +
                     u'Url:   {}\n').format(companies[i]['nazwa'],
                                            companies[i]['nazwa_skrocona'],
                                            companies[i]['nip'],
                                            companies[i]['adres'],
                                            companies[i]['url'])
                shareholders = shareholders_to_str(krs, companies[i]['id'], '')
                if shareholders:
                    description += u'Wspólnicy:\n{}'.format(shareholders)
                description += '\n'

            create_bot_report(product, description)

    except (mojepanstwo_api.CompanyNotFound, mojepanstwo_api.ConnectionError,
            mojepanstwo_api.ApiError):
        pass

    return False


def create_bot_report(product, description):
    report = Report(description=description)
    report.product = product
    report.client = 'krs-bot'
    report.save()


def serialize_product(product):
    json = {'plScore': None,
            'verified': False,
            'report': 'ask_for_company',
            'id': product.id,
            'code': product.code}

    company = product.company

    if company:
        json['report'] = False
        json['company'] = {}
        json['company']['name'] = company.common_name or \
            company.official_name or company.name
        json['company']['plCapital'] = company.plCapital
        json['company']['plCapital_notes'] = company.plCapital_notes
        json['company']['plWorkers'] = company.plWorkers
        json['company']['plWorkers_notes'] = company.plWorkers_notes
        json['company']['plRnD'] = company.plRnD
        json['company']['plRnD_notes'] = company.plRnD_notes
        json['company']['plRegistered'] = company.plRegistered
        json['company']['plRegistered_notes'] = company.plRegistered_notes
        json['company']['plNotGlobEnt'] = company.plNotGlobEnt
        json['company']['plNotGlobEnt_notes'] = company.plNotGlobEnt_notes

        plScore = get_plScore(company)
        if plScore:
            json['plScore'] = plScore
            json['verified'] = company.verified
    else:
        for prefix in CODE_PREFIX_TO_COUNTRY.keys():
            if product.code.startswith(prefix):
                json['plScore'] = 0
                json['verified'] = False
                json['company'] = {}
                json['company']['name'] = 'Miejsce rejestracji: {}' \
                    .format(CODE_PREFIX_TO_COUNTRY[prefix])

    return json


def get_plScore(company):
    if company.plCapital is not None and \
       company.plWorkers is not None and \
       company.plRnD is not None and \
       company.plRegistered is not None and \
       company.plNotGlobEnt is not None:
        return int(
            .35 * company.plCapital +
            .30 * company.plWorkers +
            .15 * company.plRnD +
            .10 * company.plRegistered +
            .10 * company.plNotGlobEnt
        )
    else:
        return None


def shareholders_to_str(krs, id, indent):
    str = ''
    json = krs.query_shareholders(id)
    data = json['data']
    kapital_zakladowy = data['krs_podmioty.wartosc_kapital_zakladowy']
    wspolnicy = json['layers']['wspolnicy']
    for wspolnik in wspolnicy:
        udzialy_wartosc = wspolnik.get('udzialy_wartosc', None)
        if udzialy_wartosc is None:
            str += u'{0}* {1} -------\n'.format(indent, wspolnik['nazwa'])
        else:
            str += u'{0}* {1} {2}/{3} {4:.0f}%\n'. \
                format(indent,
                       wspolnik['nazwa'],
                       udzialy_wartosc,
                       kapital_zakladowy,
                       100 * locale.atof(udzialy_wartosc) / kapital_zakladowy)
        if wspolnik['krs_id'] is not None:
            str += shareholders_to_str(krs, wspolnik['krs_id'], indent + '  ')
    return str


def rem_dbl_newlines(str):
    return str.replace(u'\r\n\r\n',u'\r\n').replace(u'\n\n',u'\n')

def strip_dbl_spaces(str):
    return re.sub(' +', ' ', str).strip()

def ilim_compare_str(s1, s2):
    s1 = strip_dbl_spaces(s1)
    s2 = strip_dbl_spaces(s2)
    return s1.upper() == s2.upper()

def strip_urls_newlines(str):
    s = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', '', str)
    s = rem_dbl_newlines(s)
    s = s.strip(' \t\n\r')
    return s


TYPE_RED = 'type_red'
TYPE_WHITE = 'type_white'
TYPE_GREY = 'type_grey'

DEFAULT_RESULT = {
    'product_id': None,
    'code': None,
    'name': None,
    'card_type': TYPE_WHITE,
    'plScore': None,

    'altText': None,

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

    'report_text': 'Zgłoś jeśli posiadasz bardziej aktualne dane na temat '
                   'tego produktu',
    'report_button_text': 'Zgłoś',
    'report_button_type': TYPE_WHITE,
}

DEFAULT_STATS = {
    'was_verified': False,
    'was_590': False,
    'was_plScore': False
}

CODE_PREFIX_TO_COUNTRY = {
    "30": "Francja",
    "31": "Francja",
    "32": "Francja",
    "33": "Francja",
    "34": "Francja",
    "35": "Francja",
    "36": "Francja",
    "37": "Francja",
    "380": "Bułgaria",
    "383": "Słowenia",
    "385": "Chorwacja",
    "387": "Bośnia-Hercegowina",
    "40": "Niemcy",
    "41": "Niemcy",
    "42": "Niemcy",
    "43": "Niemcy",
    "44": "Niemcy",
    "45": "Japonia",
    "46": "Federacja Rosyjska",
    "470": "Kirgistan",
    "471": "Taiwan",
    "474": "Estonia",
    "475": "Łotwa",
    "476": "Azerbejdżan",
    "477": "Litwa",
    "478": "Uzbekistan",
    "479": "Sri Lanka",
    "480": "Filipiny",
    "481": "Białoruś",
    "482": "Ukraina",
    "484": "Mołdova",
    "485": "Armenia",
    "486": "Gruzja",
    "487": "Kazachstan",
    "489": "Hong Kong",
    "49": "Japonia",
    "50": "Wielka Brytania",
    "520": "Grecja",
    "528": "Liban",
    "529": "Cypr",
    "531": "Macedonia",
    "535": "Malta",
    "539": "Irlandia",
    "54": "Belgia & Luksemburg",
    "560": "Portugalia",
    "569": "Islandia",
    "57": "Dania",
    # "590": "Polska",
    "594": "Rumunia",
    "599": "Węgry",
    "600": "Południowa Afryka",
    "601": "Południowa Afryka",
    "608": "Bahrain",
    "609": "Mauritius",
    "611": "Maroko",
    "613": "Algeria",
    "619": "Tunezja",
    "621": "Syria",
    "622": "Egipt",
    "624": "Libia",
    "625": "Jordania",
    "626": "Iran",
    "627": "Kuwejt",
    "628": "Arabia Saudyjska",
    "64": "Finlandia",
    "690": "Chiny",
    "691": "Chiny",
    "692": "Chiny",
    "70": "Norwegia",
    "729": "Izrael",
    "73": "Szwecja",
    "740": "Gwatemala",
    "741": "Salwador",
    "742": "Honduras",
    "743": "Nikaragua",
    "744": "Kostaryka",
    "745": "Panama",
    "746": "Dominikana",
    "750": "Meksyk",
    "759": "Wenezuela",
    "76": "Szwajcaria",
    "770": "Kolumbia",
    "773": "Urugwaj",
    "775": "Peru",
    "777": "Boliwia",
    "779": "Argentyna",
    "780": "Chile",
    "784": "Paragwaj",
    "786": "Ekwador",
    "789": "Brazylia",
    "790": "Brazylia",
    "80": "Włochy",
    "81": "Włochy",
    "82": "Włochy",
    "83": "Włochy",
    "84": "Hiszpania",
    "850": "Kuba",
    "858": "Słowacja",
    "859": "Czechy",
    "860": "Jugosławia",
    "867": "Korea Północna",
    "869": "Turcja",
    "87": "Holandia",
    "880": "Korea Południowa",
    "885": "Tajlandia",
    "888": "Singapur",
    "890": "Indie",
    "893": "Wietnam",
    "899": "Indonezja",
    "90": "Austria",
    "91": "Austria",
    "93": "Australia",
    "94": "Nowa Zelandia",
    "950": "EAN - IDA",
    "955": "Malezja",
    "958": "Makao",
}
