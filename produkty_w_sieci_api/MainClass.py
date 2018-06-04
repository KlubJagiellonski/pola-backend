import logging
import requests
import traceback
logger = logging.getLogger(__name__)


class ApiError(Exception):
    pass


class ConnectionError(ApiError):
    pass


class Client:
    PROD_HOST = 'https://www.produktywsieci.gs1.pl'

    def __init__(self, username, password, host=PROD_HOST):
        self.host = host
        self.session = requests.Session()
        self.username = username
        self.password = password

    def get_product_by_gtin(self, code):
        gtin = Client._normalize_gtin(code)
        url = self.host + "/api/products/{}?aggregation=CREDIBLE".format(gtin)
        try:
            resp = self.session.get(url=url, auth=(self.username, self.password), timeout=5)
        except requests.exceptions.Timeout:
            print('Timeout while querying GS1: ',traceback.format_exc())
            return None
        logger.info('GS1 resp:' + str(resp.status_code))
        if resp.status_code != 200:
            raise ConnectionError({'status_code': resp.status_code, 'code':code, 'json':resp.json()})
        json = resp.json()
        if not json.get('GTIN', None):
            return None
        return json

    @staticmethod
    def _normalize_gtin(code):
        return code.replace('-', '').replace(' ', '')
