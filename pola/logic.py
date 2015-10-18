# -*- coding: utf-8 -*-

from company.models import Company
from product.models import Product
from mojepanstwo_api import KrsClient, ApiError, CompanyNotFound, \
    ConnectionError
from produkty_w_sieci_api import Client, ApiError
from django.conf import settings
import locale
from report.models import Report

def get_by_code(code):
    try:
        return Product.objects.get(code=code)
    except Product.DoesNotExist:
        pass
    try:
        client = Client(settings.PRODUKTY_W_SIECI_API_KEY)
        product_info = client.get_product_by_gtin(code)
        return create_from_api(code, product_info)
    except ApiError:
        pass
    return Product.objects.create(code=code)

def create_from_api(code, obj):
    obj_owner_name = None
    obj_product_name = None

    if obj:
        obj_data = obj.get('Data', {}) or {}
        obj_owner = obj_data.get('Owner', {}) or {}
        obj_owner_name = obj_owner.get('Name', None)
        obj_product = obj.get('Product', {}) or {}
        obj_product_name = obj_product.get('Name', None)

    if obj_owner_name:
        company, company_created = Company.objects.get_or_create(
            name=obj_owner_name,
            commit_desc='Firma utworzona automatycznie na podstawie API'
                        ' ILiM')

    else:
        company = None

#TODO: add commit_desc

    product = Product.objects.create(
        name=obj_product_name,
        code=code,
        company=company,
        commit_desc="Produkt utworzony automatycznie na podstawie skanu "
                    "użytkownika")

    if company and company_created:
        update_company_from_krs(product, company)

    return product


def update_company_from_krs(product, company):
    try:
        krs = KrsClient()
        companies = krs.get_companies_by_name(company.name)
        if companies.__len__() == 1:
            company.official_name = companies[0]['nazwa']
            company.common_name = companies[0]['nazwa_skrocona']
            company.address = companies[0]['adres']
            company.nip = companies[0]['nip']
            company.plRegistered = 100

            Company.save(company, commit_desc=
                "Dane firmy pobrane automatycznie poprzez API "
                "mojepanstwo.pl ({})"
                         .format(companies[0]['url'])
                )

            shareholders = shareholders_to_str(krs, companies[0]['id'] ,'')
            if shareholders:
                create_bot_report(product, u'Wspólnicy spółki {}:\n{}'.
                                  format(company.name, shareholders))


        elif companies.__len__() > 0:
            description = u'{} - ta firma może być jedną z następujących:\n\n'\
                .format(company.name)

            for i in range(0,min(companies.__len__(),10)):
                description +=\
                    (u'Nazwa: {}\n'+\
                u'Skrót: {}\n'+\
                u'NIP:   {}\n'+\
                u'Adres: \n{}\n'+\
                u'Url:   {}\n').format(companies[i]['nazwa'],
                                   companies[i]['nazwa_skrocona'],
                                   companies[i]['nip'],
                                   companies[i]['adres'],
                                   companies[i]['url'])
                shareholders = shareholders_to_str(krs, companies[i]['id'] ,'')
                if shareholders:
                    description += u'Wspólnicy:\n{}'.format(shareholders)
                description+='\n'

            create_bot_report(product, description)

    except (CompanyNotFound, ConnectionError, ApiError):
        pass

def create_bot_report(product, description):
    report = Report(description = description)
    report.product = product
    report.client = 'krs-bot'
    report.save()

def serialize_product(product):
    json = {'plScore':None,
            'verified':False,
            'report':'ask_for_company',
            'id':product.id,
            'code':product.code}

    company = product.company

    if company:
        json['report'] = False
        json['company'] = {}
        json['company']['name'] = company.common_name or company.official_name \
                                  or company.name
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

#TODO: remove after apps start using new API
        json['company']['plTaxes'] = 0
        json['company']['plTaxes_notes'] = None
        json['company']['plBrand'] = 0
        json['company']['plBrand_notes'] = None

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
                json['company']['name'] = 'Miejsce produkcji: {}'\
                    .format(CODE_PREFIX_TO_COUNTRY[prefix])

    return json

def get_plScore(company):
    if  company.plCapital is not None and\
        company.plWorkers is not None and\
        company.plRnD is not None and\
        company.plRegistered is not None and\
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
    data = json['object']['data']
    kapital_zakladowy = data['krs_podmioty.wartosc_kapital_zakladowy']
    wspolnicy = json['object']['layers']['wspolnicy']
    for wspolnik in wspolnicy:
        udzialy_wartosc = wspolnik.get('udzialy_wartosc', None)
        if udzialy_wartosc == None:
            str+= u'{0}* {1} -------\n'.format(indent, wspolnik['nazwa'])
        else:
            str+= u'{0}* {1} {2}/{3} {4:.0f}%\n'.format(indent,
                    wspolnik['nazwa'],udzialy_wartosc,kapital_zakladowy,
                    100*locale.atof(udzialy_wartosc)/kapital_zakladowy)
        if wspolnik['krs_id'] != None:
            str+=shareholders_to_str(krs, wspolnik['krs_id'], indent+'  ')
    return str

CODE_PREFIX_TO_COUNTRY = {
            "30" : "Francja",
            "31" : "Francja",
            "32" : "Francja",
            "33" : "Francja",
            "34" : "Francja",
            "35" : "Francja",
            "36" : "Francja",
            "37" : "Francja",
            "380" : "Bułgaria",
            "383" : "Słowenia",
            "385" : "Chorwacja",
            "387" : "Bośnia-Hercegowina",
            "40" : "Niemcy",
            "41" : "Niemcy",
            "42" : "Niemcy",
            "43" : "Niemcy",
            "44" : "Niemcy",
            "45" : "Japonia",
            "46" : "Federacja Rosyjska",
            "470" : "Kirgistan",
            "471" : "Taiwan",
            "474" : "Estonia",
            "475" : "Łotwa",
            "476" : "Azerbejdżan",
            "477" : "Litwa",
            "478" : "Uzbekistan",
            "479" : "Sri Lanka",
            "480" : "Filipiny",
            "481" : "Białoruś",
            "482" : "Ukraina",
            "484" : "Mołdova",
            "485" : "Armenia",
            "486" : "Gruzja",
            "487" : "Kazachstan",
            "489" : "Hong Kong",
            "49" : "Japonia",
            "50" : "Wielka Brytania",
            "520" : "Grecja",
            "528" : "Liban",
            "529" : "Cypr",
            "531" : "Macedonia",
            "535" : "Malta",
            "539" : "Irlandia",
            "54" : "Belgia & Luksemburg",
            "560" : "Portugalia",
            "569" : "Islandia",
            "57" : "Dania",
#            "590" : "Polska",
            "594" : "Rumunia",
            "599" : "Węgry",
            "600" : "Południowa Afryka",
            "601" : "Południowa Afryka",
            "608" : "Bahrain",
            "609" : "Mauritius",
            "611" : "Maroko",
            "613" : "Algeria",
            "619" : "Tunezja",
            "621" : "Syria",
            "622" : "Egipt",
            "624" : "Libia",
            "625" : "Jordania",
            "626" : "Iran",
            "627" : "Kuwejt",
            "628" : "Arabia Saudyjska",
            "64" : "Finlandia",
            "690" : "Chiny",
            "691" : "Chiny",
            "692" : "Chiny",
            "70" : "Norwegia",
            "729" : "Izrael",
            "73" : "Szwecja",
            "740" : "Gwatemala",
            "741" : "Salwador",
            "742" : "Honduras",
            "743" : "Nikaragua",
            "744" : "Kostaryka",
            "745" : "Panama",
            "746" : "Dominikana",
            "750" : "Meksyk",
            "759" : "Wenezuela",
            "76" : "Szwajcaria",
            "770" : "Kolumbia",
            "773" : "Urugwaj",
            "775" : "Peru",
            "777" : "Boliwia",
            "779" : "Argentyna",
            "780" : "Chile",
            "784" : "Paragwaj",
            "786" : "Ekwador",
            "789" : "Brazylia",
            "790" : "Brazylia",
            "80" : "Włochy",
            "81" : "Włochy",
            "82" : "Włochy",
            "83" : "Włochy",
            "84" : "Hiszpania",
            "850" : "Kuba",
            "858" : "Słowacja",
            "859" : "Czechy",
            "860" : "Jugosławia",
            "867" : "Korea Północna",
            "869" : "Turcja",
            "87" : "Holandia",
            "880" : "Korea Południowa",
            "885" : "Tajlandia",
            "888" : "Singapur",
            "890" : "Indie",
            "893" : "Wietnam",
            "899" : "Indonezja",
            "90" : "Austria",
            "91" : "Austria",
            "93" : "Australia",
            "94" : "Nowa Zelandia",
            "950" : "EAN - IDA",
            "955" : "Malezja",
            "958" : "Makao",
}

