from random import random
from time import sleep
from typing import Optional, Union

import requests
from django.conf import settings
from pydantic import BaseModel


class ApiException(Exception):
    pass


class CompanyBase(BaseModel):
    name: str
    nip: str
    street: str
    webPage: str
    city: str
    postalCode: str


class ProductBase(BaseModel):
    id: str
    gtinNumber: str
    name: str
    targetMatket: Optional[list[str]]
    netVolume: Optional[float]
    unit: Optional[str]
    description: Optional[str]
    descriptionLanguage: str
    brand: Optional[str]
    isPublic: bool
    gpc: str
    productPage: Optional[str]
    imageUrls: list[str]
    lastModified: str
    company: Optional[CompanyBase]


class NoResult(BaseModel):
    result: str


class ProductQueryResult(BaseModel):
    count: int
    next: Optional[str]
    previous: Optional[str]
    # fucets:
    results: Union[list[ProductBase], list[NoResult]]


class ProduktyWSieciClient:
    def __init__(self, api_token: str, base_url: str = "https://www.eprodukty.gs1.pl/external_api/v1/"):
        self._api_token = api_token
        self._base_url = base_url

    def get_products(
        self,
        *,
        last_modified__gte: Optional[str] = None,
        name__contains: Optional[str] = None,
        gtin_number__prefix: Optional[str] = None,
        brand__contains: Optional[str] = None,
        gpc_number: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        num_retries: Optional[int] = 5,
    ) -> ProductQueryResult:
        uri = self._base_url.rstrip("/") + "/products/"
        params = {
            "last_modified__gte": last_modified__gte,
            "name__contains": name__contains,
            "gtin_number__prefix": gtin_number__prefix,
            "brand__contains": brand__contains,
            "gpc_number": gpc_number,
            "limit": limit,
            "offset": offset,
        }

        response = self._send_request('get', uri, params=params, num_retries=num_retries)
        return ProductQueryResult.parse_obj(response)

    def _send_request(self, method, url, *, num_retries, **kwargs):
        kwargs.setdefault('headers', {})
        kwargs['headers']['X-API-Key'] = self._api_token

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
                if 'message' in response_json:
                    raise ApiException(response_json['message'])
                break

            return response_json


if 'BASE_URL' in settings.PRODUKTY_W_SIECI:
    produkty_w_sieci_client = ProduktyWSieciClient(
        api_token=settings.GET_RESPONSE['API_TOKEN'], base_url=settings.PRODUKTY_W_SIECI['BASE_URL']
    )
else:
    produkty_w_sieci_client = ProduktyWSieciClient(api_token=settings.PRODUKTY_W_SIECI['API_TOKEN'])
