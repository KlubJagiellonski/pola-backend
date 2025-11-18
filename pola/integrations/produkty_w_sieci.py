from random import random
from time import sleep
from typing import Optional

import requests
from django.conf import settings
from pydantic import BaseModel

NOT_FOUND_ERRORMSG = "not_found"


class ApiException(Exception):
    pass


class CompanyBase(BaseModel):
    name: str
    nip: Optional[str]
    street: Optional[str]
    webPage: Optional[str]
    city: Optional[str]
    postalCode: Optional[str]


class GpcBase(BaseModel):
    code: str
    text: Optional[str]


class ProductBase(BaseModel):
    gtinNumber: str
    gtinStatus: Optional[str]
    name: Optional[str]
    targetMarket: list[str]
    netContent: list[str]
    description: Optional[str]
    descriptionLanguage: Optional[str]
    imageUrls: list[str]
    productPage: Optional[str]
    isPublic: Optional[bool]
    isVerified: Optional[bool]
    lastModified: Optional[str]
    gpc: list[GpcBase]
    brand: Optional[str]
    company: Optional[CompanyBase]


class NoResult(BaseModel):
    result: str


class ProduktyWSieciClient:
    def __init__(self, api_token: str, base_url: str = "https://www.eprodukty.gs1.pl/external_api/v2/"):
        self._api_token = api_token
        self._base_url = base_url

    def get_products(
        self,
        *,
        gtin_number: str,
        num_retries: Optional[int] = 5,
    ) -> Optional[ProductBase]:
        uri = self._base_url.rstrip("/") + "/products/" + gtin_number + "?include_local_data=true"
        params = {}

        response = self._send_request('get', uri, params=params, num_retries=num_retries)
        return None if response is None else ProductBase.parse_obj(response)

    def _send_request(self, method, url, *, num_retries, **kwargs):
        kwargs.setdefault('headers', {})
        kwargs['headers']['X-API-KEY'] = self._api_token

        with requests.Session() as session:
            for retry_num in range(num_retries + 1):
                if retry_num > 0:
                    # Sleep before retrying.
                    sleep_time = random() * 2**retry_num / 4
                    sleep(sleep_time)
                try:
                    exception = None
                    response = session.request(method, url, **kwargs)
                    response.raise_for_status()
                except requests.HTTPError as http_error:
                    exception = http_error

                if exception:
                    if retry_num == num_retries or 400 <= response.status_code < 500:
                        raise exception
                    else:
                        continue

                response_json = response.json()
                if 'errors' in response_json:
                    errorTable = response_json['errors']
                    if errorTable and isinstance(errorTable, list) and errorTable[0]['message']:
                        if errorTable[0]['message'] == NOT_FOUND_ERRORMSG:
                            return None
                        else:
                            raise ApiException(errorTable[0]['message'])
                    else:
                        raise ApiException('Unknown error response: ' + errorTable)
                break
            return response_json


if 'BASE_URL' in settings.PRODUKTY_W_SIECI:
    produkty_w_sieci_client = ProduktyWSieciClient(
        api_token=settings.PRODUKTY_W_SIECI['API_TOKEN'], base_url=settings.PRODUKTY_W_SIECI['BASE_URL']
    )
else:
    produkty_w_sieci_client = ProduktyWSieciClient(api_token=settings.PRODUKTY_W_SIECI['API_TOKEN'])
