#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import requests
logger = logging.getLogger(__name__)

class ApiError(Exception):
    pass

class ConnectionError(ApiError):
    pass

class CompanyNotFound(Exception):
    pass

class KrsClient:
    API_URL = 'https://api.mojepanstwo.pl/krs/podmioty'

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

        json = resp.json()
        if json['search'] == None or json['search']['dataobjects'] == None:
            raise ApiError()

        return json

    def get_companies_by_name(self, name):
        normalized_name = KrsClient._normalize_name(name)

        json = self.query_podmiot('conditions[nazwa]', normalized_name)

        if json['search']['dataobjects'].__len__() != 1:
            json = self.query_podmiot('q', normalized_name)
            if json['search']['dataobjects'].__len__() == 0:
                raise CompanyNotFound()

        companies = []
        for i in range(0,json['search']['dataobjects'].__len__()):
            data = json['search']['dataobjects'][i]['data']

            company = dict()
            company['nazwa'] = data['krs_podmioty.nazwa']
            company['nazwa_skrocona'] = data['krs_podmioty.nazwa_skrocona']
            company['nip'] = data['krs_podmioty.nip']
            lokal = u" lok. {}".format(data['krs_podmioty.adres_lokal']) if \
                data['krs_podmioty.adres_lokal'] else u""
            company['adres'] = u"ul. {} {} {}\n{} {}\n{}".format(
                data['krs_podmioty.adres_ulica'],
                data['krs_podmioty.adres_numer'],
                lokal,
                data['krs_podmioty.adres_kod_pocztowy'],
                data['krs_podmioty.adres_miejscowosc'],
                data['krs_podmioty.adres_kraj']
            )
            company['id'] = data['krs_podmioty.id']
            company['liczba_wspolnikow'] = \
                data['krs_podmioty.liczba_wspolnikow']

            company['score'] = json['search']['dataobjects'][i]['score']
            company['url'] = json['search']['dataobjects'][i]['_mpurl']

            companies.append(company)

        return companies

    COMMON_COMPANY_NAME_ENDINGS = \
        ( u' S.A.', u' SPÓŁKA AKCYJNA',
          u' Sp. z o.o.',u' SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ',
          u' Spółka z o.o.',u' SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ',
          u'Sp. Jawna', u'SPÓŁKA JAWNA',
          u'spółka z ograniczoną odpowiedzialnością sp.k.',
          u'SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ SPÓŁKA KOMANDYTOWA',
          u'sp. z o. o. sp.k.',
          u'SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ SPÓŁKA KOMANDYTOWA',
          u'Sp. z o.o. sp.k.',
          u'SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ SPÓŁKA KOMANDYTOWA',
          u'sp. z o.o. sp. k.',
          u'SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ SPÓŁKA KOMANDYTOWA',

    )

    @staticmethod
    def _normalize_name(name):
        name = name.upper()
        for i in range(len(KrsClient.COMMON_COMPANY_NAME_ENDINGS)/2):
            if name.endswith(KrsClient.COMMON_COMPANY_NAME_ENDINGS[i*2]
                    .upper()):
                return name[:len(name)-
                             len(KrsClient.COMMON_COMPANY_NAME_ENDINGS[i*2])]\
                       +KrsClient.COMMON_COMPANY_NAME_ENDINGS[i*2+1].upper()
        return name

    def query_shareholders(self, id):
        params = {
            'layers': 'wspolnicy'
            }
        resp = self.session.get(url=self.url+'/'+id, params=params)

        if resp.status_code != 200:
            raise ConnectionError({'status_code': resp.status_code})

        json = resp.json()
        try:
            if json['object'] is None or json['object']['layers'] is None \
                    or json['object']['data'] is None \
                    or json['object']['layers']['wspolnicy'] is None:
                raise ApiError()
        except:
            raise ApiError()

        return json