import logging
import requests
logger = logging.getLogger(__name__)


class ApiError(Exception):
    pass


class ConnectionError(ApiError):
    pass


class Client:
    PROD_HOST = 'http://api3.produktywsieci.pl/PublicService.svc/rest/json/'

    def __init__(self, api_key, host=PROD_HOST):
        self.api_key = api_key
        self.host = host
        self.session = requests.Session()

    def get_product_by_gtin(self, code):
        url = self.host + "GetExpandedProductByGTIN"
        params = {
            'gs1Key': self.api_key,
            'gtin': Client._normalize_gtin(code)
        }
        resp = self.session.get(url=url, params=params)
        # import ipdb; ipdb.set_trace()
        logger.info('GS1 resp:' + str(resp.status_code))
        if resp.status_code != 200:
            raise ConnectionError({'status_code': resp.status_code})
        json = resp.json()
        if not json.get('IsValid', False):
            return None
        return json

    @staticmethod
    def _normalize_gtin(code):
        return code.replace('-', '').replace(' ', '')
