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
    API_URL = 'https://api-v3.mojepanstwo.pl/dane/krs_podmioty'

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

        if json['Dataobject'] is None:
            raise ApiError()

        return json

    def json_to_company(self, json, i):
        data = json['Dataobject'][i]['data']

        company = dict()
        company['nazwa'] = KrsClient.unescape(data['krs_podmioty.nazwa'])
        company['nazwa_skrocona'] = \
            KrsClient.unescape(data['krs_podmioty.nazwa_skrocona'])
        company['nip'] = data['krs_podmioty.nip']
        lokal = u" lok. {}".format(data['krs_podmioty.adres_lokal']) if \
            data['krs_podmioty.adres_lokal'] else u""
        company['adres'] = KrsClient.unescape(u"ul. {} {} {}\n{} {}\n{}".format(
            data['krs_podmioty.adres_ulica'],
            data['krs_podmioty.adres_numer'],
            lokal,
            data['krs_podmioty.adres_kod_pocztowy'],
            data['krs_podmioty.adres_miejscowosc'],
            data['krs_podmioty.adres_kraj'])
        )
        company['id'] = data['krs_podmioty.id']
        company['liczba_wspolnikow'] = \
            data['krs_podmioty.liczba_wspolnikow']

        company['score'] = json['Dataobject'][i]['score']
        company['url'] = json['Dataobject'][i]['mp_url']

        return company

    def get_companies_by_name(self, name):
        normalized_name = KrsClient._normalize_name(name)

        json = self.query_podmiot('conditions[krs_podmioty.nazwa]', normalized_name)

        if json['Dataobject'].__len__() != 1:
            json = self.query_podmiot('conditions[q]', normalized_name)
            if ['Dataobject'].__len__() == 0:
                raise CompanyNotFound()

        return self.get_companies_by_json(json)

    def get_companies_by_nip(self, nip):
        json = self.query_podmiot('conditions[krs_podmioty.nip]', nip)

        return self.get_companies_by_json(json)

    def get_companies_by_json(self, json):
        companies = []
        for i in range(0, json['Dataobject'].__len__()):
            company = self.json_to_company(json, i)
            companies.append(company)

        return companies

    # remove unnecessary mojepanstwo escape
    @staticmethod
    def unescape(s):
        return s.replace('&amp;', '&')

    COMMON_COMPANY_NAME_ENDINGS = \
        {
            u' S.A.':
                u' SPÓŁKA AKCYJNA',
            u' Sp. z o.o.':
                u' SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ',
            u' Spółka z o.o.':
                u' SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ',
            u'Sp. Jawna':
                u'SPÓŁKA JAWNA',
            u'spółka z ograniczoną odpowiedzialnością sp.k.':
                u'SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ SPÓŁKA KOMANDYTOWA',
            u'sp. z o. o. sp.k.':
                u'SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ SPÓŁKA KOMANDYTOWA',
            u'Sp. z o.o. sp.k.':
                u'SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ SPÓŁKA KOMANDYTOWA',
            u'sp. z o.o. sp. k.':
                u'SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ SPÓŁKA KOMANDYTOWA'
          }

    @staticmethod
    def _normalize_name(name):
        name = name.upper()
        for key, value in KrsClient.COMMON_COMPANY_NAME_ENDINGS.items():
            if name.endswith(key.upper()):
                return name[:len(name) - len(key)] + value
        return name

    def query_shareholders(self, id):
        params = {'layers': 'wspolnicy'}
        resp = self.session.get(url=self.url + '/' + id, params=params)

        if resp.status_code != 200:
            raise ConnectionError({'status_code': resp.status_code})

        json = resp.json()
        try:
            if json['layers'] is None or json['layers']['wspolnicy'] is None:
                raise ApiError()
        except KeyError:
            raise ApiError()

        return json
