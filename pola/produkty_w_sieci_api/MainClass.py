import logging
import traceback

import requests
import urllib3
from gtin import GTIN, CheckDigitError

logger = logging.getLogger(__name__)


class ApiError(Exception):
    pass


class ConnectionError(ApiError):
    pass


def is_code_supported_by_gs1_api(code):
    code = code.lstrip('0')

    try:
        GTIN(code)
    except CheckDigitError:
        return False

    if (
        code.isdigit()
        and len(code) in [8, 11, 12, 13, 14]
        and not code.startswith(('190', '967', '977', '978', '979', '99', '150', '169', '2', '922', '178', '161'))
    ):
        return True

    return False


class Client:
    PROD_HOST = 'https://www.produktywsieci.gs1.pl'

    def __init__(self, username, password, host=PROD_HOST):
        self.host = host
        self.session = requests.Session()
        self.username = username
        self.password = password

    def get_product_by_gtin(self, code):
        gtin = Client._normalize_gtin(code)
        url = self.host + f"/api/products/{gtin}?aggregation=CREDIBLE"
        try:
            resp = self.session.get(url=url, auth=(self.username, self.password), timeout=10)
        except (requests.exceptions.Timeout, urllib3.exceptions.ReadTimeoutError):
            print('Timeout while querying GS1: ', traceback.format_exc())
            return None
        logger.info('GS1 resp:' + str(resp.status_code))
        if resp.status_code != 200:
            raise ConnectionError({'status_code': resp.status_code, 'code': code, 'json': resp.json()})
        json = resp.json()
        if not json.get('GTIN', None):
            return None
        return json

    @staticmethod
    def _normalize_gtin(code):
        return code.replace('-', '').replace(' ', '')
