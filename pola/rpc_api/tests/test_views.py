import json

from django.conf import settings


class JsonRequestMixin:
    def json_request(self, url, data=None, **kwargs):
        body = json.dumps(data)
        token = getattr(settings, 'SET_BEARER_TOKEN', None)
        if token and 'HTTP_AUTHORIZATION' not in kwargs:
            kwargs['HTTP_AUTHORIZATION'] = f'Bearer {token}'
        return self.client.post(url, body, content_type="application/json", **kwargs)
