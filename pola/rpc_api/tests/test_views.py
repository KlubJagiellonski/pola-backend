import json


class JsonRequestMixin:
    def json_request(self, url, data=None, **kwargs):
        body = json.dumps(data)
        return self.client.post(url, body, content_type="application/json", **kwargs)
