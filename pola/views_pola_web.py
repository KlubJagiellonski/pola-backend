import functools
from pathlib import Path

from django.conf import settings
from django.http import HttpResponse
from django.utils.cache import add_never_cache_headers
from django.utils.decorators import method_decorator
from django.views import View, defaults
from django.views.decorators.cache import cache_page
from django.views.decorators.gzip import gzip_page
from django.views.decorators.http import condition

from google.api_core import exceptions as gcs_exceptions

from pola.gcs import get_bucket

# 256 KB
MAX_CACHE_KEY_SIZE = int(256 * 1024)
# 15 minutes
CACHE_TIMEOUT = 60 * 15


def get_candidates(file_path):
    file_path = file_path.strip("/")
    if file_path == "":
        return ["index.html"]
    candidates = []
    if file_path:
        candidates.append(file_path)
    splited_path = Path(file_path).suffix
    if not splited_path:
        candidates.append(file_path + "/index.html")
        # używamy GCS, a nie lokalnego filesystemu, więc nie powinniśmy używać os.path.join
        # bo i tak separatorem ścieżki w GCS jest zawsze /
    return candidates


@functools.lru_cache
def head_object(filepath):
    bucket = get_bucket(settings.GCS_WEB_BUCKET_NAME)
    for candidate_key in get_candidates(filepath):
        try:
            hash_key = candidate_key
            if settings.USE_ESCAPED_GCS_PATHS and ('\\' in candidate_key):
                hash_key = candidate_key.replace("\\", "___")
            blob = bucket.get_blob(hash_key)
            if blob:
                return blob
        except gcs_exceptions.NotFound:
            continue
    return None


def get_etag(request):
    blob = head_object(request.path)
    return blob.etag if blob else None


def get_last_modified(request):
    blob = head_object(request.path)
    return blob.updated if blob else None


@method_decorator(gzip_page, name='dispatch')
@method_decorator(condition(etag_func=get_etag, last_modified_func=get_last_modified), name='dispatch')
@method_decorator(cache_page(CACHE_TIMEOUT), name='dispatch')
class PolaWebView(View):
    def get_gcs_response(self, key, status_code=200):
        try:
            blob = get_bucket(settings.GCS_WEB_BUCKET_NAME).blob(key)
            body = blob.download_as_bytes()
            content_type = blob.content_type or 'application/octet-stream'
            return HttpResponse(body, content_type=content_type, status=status_code)
        except gcs_exceptions.NotFound:
            return None

    def get(self, request):
        if request.path.startswith('/cms/'):
            return defaults.page_not_found(request, self.kwargs.get('exception', None))
        blob = head_object(request.path)
        if blob:
            gcs_response = self.get_gcs_response(blob.name, status_code=200)
            if gcs_response:
                if len(gcs_response.content) > MAX_CACHE_KEY_SIZE:
                    add_never_cache_headers(gcs_response)
                return gcs_response
        else:
            gcs_response = self.get_gcs_response('404.html', status_code=404)
            if gcs_response:
                return gcs_response

        return defaults.page_not_found(request, self.kwargs.get('exception', None))


page_not_found_handler = PolaWebView.as_view()
