# -*- coding: utf-8 -*-

from company.models import Company

def serialize_product(product):
    json = {'plScore':None,
            'verified':False,
            'id':product.id}

    company = product.company

    if company:

        json['company'] = {}
        json['company']['name'] = company.common_name \
            if company.common_name \
            else company.official_name if company.official_name \
            else company.name
        json['company']['plRnD'] = company.plRnD
        json['company']['plRnD_notes'] = company.plRnD_notes
        json['company']['plWorkers'] = company.plWorkers
        json['company']['plWorkers_notes'] = company.plWorkers_notes
        json['company']['plCapital'] = company.plCapital
        json['company']['plCapital_notes'] = company.plCapital_notes
        json['company']['plTaxes'] = company.plTaxes
        json['company']['plTaxes_notes'] = company.plTaxes_notes
        json['company']['plBrand'] = company.plBrand
        json['company']['plBrand_notes'] = company.plBrand_notes

        if company.plRnD and company.plWorkers and company.plCapital and\
            company.plTaxes and company.plBrand:
            plScore = .2 * company.plRnD / 100 + \
                    .2 * company.plWorkers / 100 + \
                    .3 * company.plCapital / 100 + \
                    .2 * company.plTaxes / 100 + \
                    .1 * company.plBrand / 100
            json['plScore'] =  int(100 * plScore)
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

