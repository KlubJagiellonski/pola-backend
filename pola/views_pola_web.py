import os

from botocore.exceptions import ClientError
from django.conf import settings
from django.http import HttpResponse
from django.utils.cache import add_never_cache_headers
from django.views import View, defaults
from django.views.decorators.cache import cache_page

from pola.s3 import create_s3_client

# 256 KB
MAX_CACHE_KEY_SIZE = int(256 * 1024)
# 15 minutes
CACHE_TIMEOUT = 60 * 15


class PolaWebView(View):
    def get_s3_data(self, s3_client, key):
        try:
            print(f"PolaWebView:get_s3_stream_response::key={key}, bucket={settings.AWS_STORAGE_WEB_BUCKET_NAME}")
            s3_obj = s3_client.get_object(
                Bucket=settings.AWS_STORAGE_WEB_BUCKET_NAME,
                Key=key,
            )
            body = s3_obj['Body'].read()
            content_type = s3_obj.get('ContentType') or 'application/octet-stream'
            return body, content_type
        except ClientError as ex:
            if ex.response['Error']['Code'] == 'NoSuchKey':
                return None
            else:
                raise

    def get(self, request):
        if request.path.startswith('/cms/'):
            return defaults.page_not_found(request, self.kwargs.get('exception', None))
        s3_client = create_s3_client()
        file_path = request.path.strip("/")
        for candidate_key, status_code in self.get_candidates(file_path):
            s3_response = self.get_s3_data(s3_client, candidate_key)
            if not s3_response:
                continue
            body, content_type = s3_response
            response = HttpResponse(body, content_type=content_type, status=status_code)
            if len(body) > MAX_CACHE_KEY_SIZE:
                add_never_cache_headers(response)
            return response

        return defaults.page_not_found(request, self.kwargs.get('exception', None))

    def get_candidates(self, file_path):
        candidates = []
        if file_path:
            candidates.append((file_path, 200))
        splited_path = os.path.splitext(file_path)
        if not splited_path[1]:
            candidates.append((os.path.join(file_path, "index.html"), 200))
        candidates.append(('404.html', 404))
        return candidates


page_not_found_handler = cache_page(CACHE_TIMEOUT)(PolaWebView.as_view())
