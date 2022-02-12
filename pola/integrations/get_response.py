from random import random
from time import sleep

import requests
from django.conf import settings


class GetResponseClient:
    def __init__(self, api_token: str, base_url: str = "https://api.getresponse.com/v3"):
        self._api_token = api_token
        self._base_url = base_url

    def create_contact(self, campaign_id, email, name=None, num_retries=5):
        print(f"create_contact: email={email} name={name}")
        uri = self._base_url + "/contacts"
        body = {
            "name": name,
            "campaign": {"campaignId": campaign_id},
            "email": email,
        }
        response = self._send_request('post', uri, num_retries=num_retries, json=body)
        return response

    def _send_request(self, method, url, *, num_retries, **kwargs):
        kwargs.setdefault('headers', {})
        kwargs['headers']['X-Auth-Token'] = f"api-key {self._api_token}"

        with requests.Session() as session:
            for retry_num in range(num_retries + 1):
                if retry_num > 0:
                    # Sleep before retrying.
                    sleep_time = random() * 2 ** retry_num
                    sleep(sleep_time)
                try:
                    exception = None
                    print(f"{method} {url}")
                    response = session.request(method, url, **kwargs)
                    print(f"response={response}")
                    response.raise_for_status()
                except requests.HTTPError as http_error:
                    exception = http_error
                    print(f"{exception} {exception.__dict__}")

                if exception:
                    if retry_num == num_retries:
                        raise exception
                    else:
                        continue
                else:
                    break

            return response


if 'BASE_URL' in settings.GET_RESPONSE:
    get_response_client = GetResponseClient(
        api_token=settings.GET_RESPONSE['API_KEY'], base_url=settings.GET_RESPONSE['BASE_URL']
    )
else:
    get_response_client = GetResponseClient(api_token=settings.GET_RESPONSE['API_KEY'])
