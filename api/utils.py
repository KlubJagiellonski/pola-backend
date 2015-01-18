# coding=utf-8
import json

import barcodenumber
from django.http import HttpResponse


def create_json_http_response(list):
    return HttpResponse(json.dumps(json_result(True, list)), content_type="application/json")


def create_error_json_http_response(error_code):
    return HttpResponse(json.dumps(json_result(False, error_code)), content_type="application/json")


def json_result(success, result):
    return {
        "success": success,
        "result": result
    }


def correct_nip(nip):
    nip = nip.strip().replace(" ", "").replace("-", "")
    if len(nip) == 10:
        nip = 'PL' + nip
    return nip


def correct_barcode(barcode):
    if len(barcode) == 13:
        return barcodenumber.check_code_ean13(barcode)
    if len(barcode) == 8:
        return barcodenumber.check_code_ean8(barcode)
    return False


country_to_number_system_map = {
    30: 'Francja',
    31: 'Francja',
    32: 'Francja',
    33: 'Francja',
    34: 'Francja',
    35: 'Francja',
    36: 'Francja',
    37: 'Francja',
    380: 'Bułgaria',
    383: 'Słowenia',
    385: 'Chorwacja',
    387: 'Bośnia-Hercegowina',
    40: 'Niemcy',
    41: 'Niemcy',
    42: 'Niemcy',
    43: 'Niemcy',
    44: 'Niemcy',
    45: 'Japonia',
    46: 'Federacja Rosyjska',
    470: 'Kirgistan',
    471: 'Taiwan',
    474: 'Estonia',
    475: 'Łotwa',
    476: 'Azerbejdżan',
    477: 'Litwa',
    478: 'Uzbekistan',
    479: 'Sri Lanka',
    480: 'Filipiny',
    481: 'Białoruś',
    482: 'Ukraina',
    484: 'Mołdova',
    485: 'Armenia',
    486: 'Gruzja',
    487: 'Kazachstan',
    489: 'Hong Kong',
    49: 'Japonia',
    50: 'Wielka Brytania',
    520: 'Grecja',
    528: 'Liban',
    529: 'Cypr',
    531: 'Macedonia',
    535: 'Malta',
    539: 'Irlandia',
    54: 'Belgia & Luksemburg',
    560: 'Portugalia',
    569: 'Islandia',
    57: 'Dania',
    590: 'Polska',
    594: 'Rumunia',
    599: 'Węgry',
    600: 'Południowa Afryka',
    601: 'Południowa Afryka',
    608: 'Bahrain',
    609: 'Mauritius',
    611: 'Maroko',
    613: 'Algeria',
    619: 'Tunezja',
    621: 'Syria',
    622: 'Egipt',
    624: 'Libia',
    625: 'Jordania',
    626: 'Iran',
    627: 'Kuwejt',
    628: 'Arabia Saudyjska',
    64: 'Finlandia',
    690: 'Chiny',
    691: 'Chiny',
    692: 'Chiny',
    70: 'Norwegia',
    729: 'Izrael',
    73: 'Szwecja',
    740: 'Gwatemala',
    741: 'Salwador',
    742: 'Honduras',
    743: 'Nikaragua',
    744: 'Kostaryka',
    745: 'Panama',
    746: 'Dominikana',
    750: 'Meksyk',
    759: 'Wenezuela',
    76: 'Szwajcaria',
    770: 'Kolumbia',
    773: 'Urugwaj',
    775: 'Peru',
    777: 'Boliwia',
    779: 'Argentyna',
    780: 'Chile',
    784: 'Paragwaj',
    786: 'Ekwador',
    789: 'Brazylia',
    790: 'Brazylia',
    80: 'Włochy',
    81: 'Włochy',
    82: 'Włochy',
    83: 'Włochy',
    84: 'Hiszpania',
    850: 'Kuba',
    858: 'Słowacja',
    859: 'Czechy',
    860: 'Jugosławia',
    867: 'Korea Północna',
    869: 'Turcja',
    87: 'Holandia',
    880: 'Korea Południowa',
    885: 'Tajlandia',
    888: 'Singapur',
    890: 'Indie',
    893: 'Wietnam',
    899: 'Indonezja',
    90: 'Austria',
    91: 'Austria',
    93: 'Australia',
    94: 'Nowa Zelandia',
    950: 'EAN - IDA',
    955: 'Malezja',
    958: 'Makao',
}


def country_name_from_number_system(number_system):
    if number_system >= 0 and number_system <= 139:
        return 'USA & Kanada'
    if number_system in country_to_number_system_map:
        return country_to_number_system_map[number_system]
    two_digit_number_system = number_system / 10
    if two_digit_number_system in country_to_number_system_map:
        return country_to_number_system_map[two_digit_number_system]
    return 'Nieznany'