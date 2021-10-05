import functools
import os

from botocore.exceptions import ClientError
from django.conf import settings
from django.http import HttpResponse
from django.utils.cache import add_never_cache_headers
from django.utils.decorators import method_decorator
from django.views import View, defaults
from django.views.decorators.cache import cache_page
from django.views.decorators.gzip import gzip_page
from django.views.decorators.http import condition

from pola.s3 import create_s3_client

# 256 KB
MAX_CACHE_KEY_SIZE = int(256 * 1024)
# 15 minutes
CACHE_TIMEOUT = 60 * 15


def get_candidates(file_path):
    file_path = file_path.strip("/")
    candidates = []
    if file_path:
        candidates.append(file_path)
    splited_path = os.path.splitext(file_path)
    if not splited_path[1]:
        candidates.append(os.path.join(file_path, "index.html"))
    return candidates


@functools.lru_cache
def head_object(filepath):
    s3_client = create_s3_client()
    for candidate_key in get_candidates(filepath):
        try:
            s3_obj = s3_client.head_object(Bucket=settings.AWS_STORAGE_WEB_BUCKET_NAME, Key=candidate_key)
            s3_obj['Key'] = candidate_key
            return s3_obj
        except ClientError as ex:
            if ex.response['Error']['Code'] in ('NoSuchKey', '404'):
                continue
            else:
                raise
    return None


def get_etag(request):
    s3_obj = head_object(request.path)
    return s3_obj.get('ETag') if s3_obj else None


def get_last_modified(request):
    s3_obj = head_object(request.path)
    return s3_obj.get('LastModified') if s3_obj else None


@method_decorator(gzip_page, name='dispatch')
@method_decorator(condition(etag_func=get_etag, last_modified_func=get_last_modified), name='dispatch')
@method_decorator(cache_page(CACHE_TIMEOUT), name='dispatch')
class PolaWebView(View):
    def get_s3_response(self, key, status_code=200):
        try:
            s3_client = create_s3_client()
            s3_obj = s3_client.get_object(
                Bucket=settings.AWS_STORAGE_WEB_BUCKET_NAME,
                Key=key,
            )
            body = s3_obj['Body'].read()
            content_type = s3_obj.get('ContentType') or 'application/octet-stream'
            return HttpResponse(body, content_type=content_type, status=status_code)
        except ClientError as ex:
            if ex.response['Error']['Code'] in ('NoSuchKey', '404'):
                return None
            else:
                raise

    def get(self, request):
        if request.path.startswith('/cms/'):
            return defaults.page_not_found(request, self.kwargs.get('exception', None))
        s3_obj = head_object(request.path)
        if s3_obj:
            s3_response = self.get_s3_response(s3_obj['Key'], status_code=200)
            if s3_response:
                if len(s3_response.content) > MAX_CACHE_KEY_SIZE:
                    add_never_cache_headers(s3_response)
                return s3_response
        else:
            s3_response = self.get_s3_response('404.html', status_code=404)
            if s3_response:
                return s3_response

        return defaults.page_not_found(request, self.kwargs.get('exception', None))


page_not_found_handler = PolaWebView.as_view()
