#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from collections import namedtuple

import requests

logger = logging.getLogger(__name__)


class ApiError(Exception):
    pass


class ConnectionError(ApiError):
    pass


CompanyInfo = namedtuple('CompanyInfo', [
    'id',
    'nazwa',
    'nazwa_skrocona',
    'nip',
    'adres',
    'liczba_wspolnikow',
    'score',
    'url']
)


class ApiClient:
    API_URL = 'https://api-v3.mojepanstwo.pl/'

    def __init__(self, url=API_URL):
        self.url = url
        self.session = requests.Session()

    def send_request(self, method, **kwargs):

        resp = self.session.get(url=self.API_URL + method, **kwargs)

        if resp.status_code != 200:
            raise ConnectionError({'status_code': resp.status_code})

        json = resp.json()

        if json['Dataobject'] is None:
            raise ApiError()

        return json


class Krs:
    def __init__(self, client=None):
        self.client = client or ApiClient()

    def get_companies(self, **kwargs):
        conditions = {}

        if 'search_terms' in kwargs:
            conditions['q'] = Krs._normalize_name(kwargs['search_terms'])

        if 'krs_name' in kwargs:
            conditions['krs_podmioty.nazwa'] = Krs._normalize_name(kwargs['krs_name'])

        if 'krs_no' in kwargs:
            conditions['krs_podmioty.krs'] = kwargs['krs_no']

        if 'krs_nip' in kwargs:
            conditions['krs_podmioty.nip'] = kwargs['krs_name']

        response = self.client.send_request('dane/krs_podmioty', conditions=conditions)
        return self._parse_companies_response(response)

    def get_companies_by_name(self, name):
        return self.get_companies(krs_name=name) or \
            self.get_companies(search_terms=name)

    def query_shareholders(self, id):
        return self.client.send_request('dane/krs_podmioty/' + id, layers='wspolnicy')

    def _parse_companies_response(self, json):
        return map(lambda o: self._json_to_company(o), json['Dataobject'])

    def _json_to_company(self, json):
        company = dict()
        company['nazwa'] = Krs._unescape(json['data']['krs_podmioty.nazwa'])
        company['nazwa_skrocona'] = \
            Krs._unescape(json['data']['krs_podmioty.nazwa_skrocona'])
        company['nip'] = json['data']['krs_podmioty.nip']
        company['adres'] = self._simplify_address(json)
        company['id'] = json['data']['krs_podmioty.id']
        company['liczba_wspolnikow'] = \
            json['data']['krs_podmioty.liczba_wspolnikow']
        company['score'] = json['score']
        company['url'] = json['mp_url']

        return CompanyInfo(**company)

    def _simplify_address(self, data):
        lokal = u" lok. {}".format(data['krs_podmioty.adres_lokal']) if \
            data['krs_podmioty.adres_lokal'] else u""
        adres = Krs._unescape(u"ul. {} {} {}\n{} {}\n{}".format(
            data['krs_podmioty.adres_ulica'],
            data['krs_podmioty.adres_numer'],
            lokal,
            data['krs_podmioty.adres_kod_pocztowy'],
            data['krs_podmioty.adres_miejscowosc'],
            data['krs_podmioty.adres_kraj'])
        )
        return adres

    # remove unnecessary mojepanstwo escape
    @staticmethod
    def _unescape(s):
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
        for key, value in Krs.COMMON_COMPANY_NAME_ENDINGS.items():
            if name.endswith(key.upper()):
                return name[:len(name) - len(key)] + value
        return name
