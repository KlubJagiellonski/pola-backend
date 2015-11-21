#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import requests
import locale
logger = logging.getLogger(__name__)

class ApiError(Exception):
    pass

class ConnectionError(ApiError):
    pass

class CompanyDoesNotExists(Exception):
    pass

class CompanyNameNotUnique(Exception):
    pass

class KrsClient:
    API_URL = 'https://api-v3.mojepanstwo.pl/krs/podmioty'

    def __init__(self, url=API_URL):
        self.url = url
        self.session = requests.Session()

    def query_podmiot(self, param, value):
        params = {
            param: value
            }
        resp = self.session.get(url=self.url, params=params)

        if resp.status_code != 200:
            raise ConnectionError({'status_code': resp.status_code})

        print resp.url

        json = resp.json()
        if json['search'] == None or json['search']['dataobjects'] == None:
            raise ApiError()

        return json

    def get_podmiot_by_name(self, name):
        normalized_name = KrsClient._normalize_name(name)

        json = self.query_podmiot('conditions[nazwa]', normalized_name)

        if json['search']['dataobjects'].__len__() != 1:
            json = self.query_podmiot('q', normalized_name)

            if json['search']['dataobjects'].__len__() == 0:
                raise CompanyDoesNotExists()

        data = json['search']['dataobjects'][0]['data']

        company = dict()
        company['nazwa'] = data['krs_podmioty.nazwa']
        company['nip'] = data['krs_podmioty.nip']
        company['score'] = json['search']['dataobjects'][0]['score']
        company['id'] = data['krs_podmioty.id']
        company['liczba_wspolnikow'] = data['krs_podmioty.liczba_wspolnikow']

        return company

    COMMON_COMPANY_NAME_ENDINGS = ( u' S.A.', u' SPÓŁKA AKCYJNA',
                                    u' Sp. z o.o.',u' SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ',
                                    u' Spółka z o.o.',u' SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ',
                                    u'Sp. Jawna', u'SPÓŁKA JAWNA',
                                    u'spółka z ograniczoną odpowiedzialnością sp.k.', u'SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ SPÓŁKA KOMANDYTOWA',
                                    u'sp. z o. o. sp.k.', u'SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ SPÓŁKA KOMANDYTOWA',
                                    u'Sp. z o.o. sp.k.', u'SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ SPÓŁKA KOMANDYTOWA',
                                    u'sp. z o.o. sp. k.', u'SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ SPÓŁKA KOMANDYTOWA',

    )

    @staticmethod
    def _normalize_name(name):
        name = name.upper()
        for i in range(len(KrsClient.COMMON_COMPANY_NAME_ENDINGS)/2):
            if name.endswith(KrsClient.COMMON_COMPANY_NAME_ENDINGS[i*2].upper()):
                return name[:len(name)-len(KrsClient.COMMON_COMPANY_NAME_ENDINGS[i*2])]+KrsClient.COMMON_COMPANY_NAME_ENDINGS[i*2+1].upper()
        return name

    def query_wspolnicy(self, id):
        params = {
            'layers': 'wspolnicy'
            }
        resp = self.session.get(url=self.url+'/'+id, params=params)

        if resp.status_code != 200:
            raise ConnectionError({'status_code': resp.status_code})
        print resp.url
        json = resp.json()
        if json['object'] == None or json['object']['layers'] == None or json['object']['data'] == None or json['object']['layers']['wspolnicy'] == None:
            raise ApiError()

        return json

    def get_wspolnicy(self, id, intent, final_wspolnicy):
        json = self.query_wspolnicy(id)
        data = json['object']['data']
        kapital_zakladowy = data['krs_podmioty.wartosc_kapital_zakladowy']
        wspolnicy = json['object']['layers']['wspolnicy']
        for wspolnik in wspolnicy:
            udzialy_wartosc = wspolnik.get('udzialy_wartosc', None)
            if udzialy_wartosc == None:
                print u'{0}* {1} -------'.format(intent, wspolnik['nazwa'])
            else:
                print u'{0}* {1} {2}/{3} {4:.0f}%'.format(intent, wspolnik['nazwa'],udzialy_wartosc,kapital_zakladowy,
                        100*locale.atof(udzialy_wartosc)/kapital_zakladowy)
            if wspolnik['krs_id'] != None:
                self.get_wspolnicy(wspolnik['krs_id'], intent+'  ', final_wspolnicy)

def print_company(name):
    client = KrsClient()
    try:
        print
        print name
        company = client.get_podmiot_by_name(name)
        print company['nazwa']
        print company['nip']
        print company['score']
        client.get_wspolnicy(company['id'], '', None)

    except CompanyDoesNotExists:
        print "Nie znaleziono"
    except CompanyNameNotUnique:
        print "Za dużo wyników"

    return

def main():
    client = KrsClient()

    print_company(u'Browar Zamkowy Cieszyn Sp. z o.o.')
    print_company(u'NIVEA Polska Spółka z ograniczoną odpowiedzialnością')
    print_company(u'MANUFAKTURA KAPUCYNÓW')
    print_company(u'Unilever Polska Sp. z o.o.')
    print_company(u'Kwaśne Jabłko Marcin Wiechowski')
    print_company(u'OBORY Sp. z o.o.')
    print_company(u'FROGUT PLASTICS Sp. z o.o.')
    print_company(u'INTER GLOBUS Sp. z o.o.')
    print_company(u'SANTE A. Kowalski Sp. Jawna')
    print_company(u'COLIAN sp. z o.o.')
    print_company(u'BAKALLAND S.A.')
    print_company(u'SUEDZUCKER POLSKA S.A.')
    print_company(u'RECKITT BENCKISER (POLAND) S.A.')
    print_company(u'FERMY KOŹLAKIEWICZ Spółka Jawna')
    print_company(u'INVEST Spółka z o.o.')
    print_company(u'Diamond Cosmetics Poland sp. z o.o.')
    print_company(u'P.P.H.U. GAJATEX-PRIM S.C. Anna Frątczak, Tomasz Grabski')
    print_company(u'KOLGLASS Hurt - Import - Export Ryszard Kolat')
    print_company(u'Animex Foods Sp. z o.o. sp.k.')
    print_company(u'Elfa Pharm Polska sp. z o.o. sp. k.')
    print_company(u'BiFIX Wojciech Piasecki Spółka Jawna')
    print_company(u'LOTTE Wedel sp. z o.o.')
    print_company(u'GLOBAL COSMED GROUP Spółka Akcyjna')
    print_company(u'Toruńskie Zakłady Materiałów Opatrunkowych S.A.')
    print_company(u'Okręgowa Spółdzielnia Mleczarska')
    print_company(u'Spółdzielnia Pracy MUSZYNIANKA')
    print_company(u'Firma Bracia Urbanek Andrzej i Jacek Urbanek Spółka Jawna')
    print_company(u'WAWEL Spółka Akcyjna')
    print_company(u'VOG Polska Sp. z o.o.')
    print_company(u'PROFIm Sp. z o.o.')
    print_company(u'GOOD FOOD PRODUCTS Sp. z o.o.')
    print_company(u'ZIAJA Ltd Zakład Produkcji Leków Sp. z o.o.')
    print_company(u'ZL NAŁĘCZÓW ZDRÓJ spółka z ograniczoną odpowiedzialnością sp.k.')
    print_company(u'Pudliszki Sp. z o.o.')
    print_company(u'Zakład Przetwórstwa Owocowo Warzywnego DAWTONA Danuta Wielgomas')
    print_company(u'Lubella Sp. z o.o. Sp. k.')
    print_company(u'Zakłady Tłuszczowe KRUSZWICA S.A.')
    print_company(u'WAWEL Spółka Akcyjna')
    print_company(u'Firma Bracia Urbanek Andrzej i Jacek Urbanek Spółka Jawna')
    print_company(u'Lubella Sp. z o.o. Sp. k.')
    print_company(u'Diamond Cosmetics Poland sp. z o.o.')
    print_company(u'Toruńskie Zakłady Materiałów Opatrunkowych S.A.')
    print_company(u'Spółdzielnia Pracy MUSZYNIANKA')
    print_company(u'COLIAN sp. z o.o.')
    print_company(u'BIO NATURA Jacek Mazurek')
    print_company(u'KOLGLASS Hurt - Import - Export Ryszard Kolat')
    print_company(u'POLSKIE MŁYNY S.A.')
    print_company(u'BiFIX Wojciech Piasecki Spółka Jawna')
    print_company(u'HARPER HYGIENICS S.A.')
    print_company(u'BAKALLAND S.A.')
    print_company(u'PROFIm Sp. z o.o.')
    print_company(u'Browar Zamkowy Cieszyn Sp. z o.o.')
    print_company(u'SANTE A. Kowalski Sp. Jawna')
    print_company(u'SUEDZUCKER POLSKA S.A.')
    print_company(u'GRUPA INCO S.A.')
    print_company(u'VOG Polska Sp. z o.o.')
    print_company(u'OBORY Sp. z o.o.')
    print_company(u'Spółdzielnia Mleczarska MLEKPOL w Grajewie')
    print_company(u'BAKOMA Sp. z o.o.')
    print_company(u'Zakład Przetwórstwa Owocowo Warzywnego DAWTONA Danuta Wielgomas')
    print_company(u'ZL NAŁĘCZÓW ZDRÓJ spółka z ograniczoną odpowiedzialnością sp.k.')
    print_company(u'Pudliszki Sp. z o.o.')
    print_company(u'Przedsiębiorstwo Produkcyjno Handlowe LEWIN Henryk Odelga')
    print_company(u'MAKRO CASH AND CARRY POLSKA S.A.')
    print_company(u'FZZPM w Polsce Zakład Usług Handlowych "ROBICO"')
    print_company(u'AGROS-NOVA Soki Sp. z o.o.')
    print_company(u'Velvet CARE sp. z o.o.')
    print_company(u'PFEIFER & LANGEN MARKETING Spółka z o.o.')
    print_company(u'Okręgowa Spółdzielnia Mleczarska w Piątnicy')
    print_company(u'Spółdzielnia Mleczarska MLEKOVITA')
    print_company(u'P.P.H.U. ASPOL Andrzej i Sylwester Szymańscy Spółka Jawna')
    print_company(u'KOMPANIA PIWOWARSKA S.A.')
    print_company(u'POLSKA WODA Sp. z o.o.')
    print_company(u'MOKATE S.A.')
    print_company(u'ŻYWIEC ZDRÓJ S.A.')
    print_company(u'BIO NATURA Jacek Mazurek')


if __name__ == "__main__":
    main()
