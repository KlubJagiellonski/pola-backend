import os

from botocore.exceptions import ClientError
from django.conf import settings
from django.http import HttpResponse
from django.views import View, defaults
from django.views.decorators.cache import cache_page

from pola.s3 import create_s3_client


class PolaWebView(View):
    def get_s3_stream_response(self, s3_client, key, status_code=200):
        try:
            print(f"PolaWebView:get_s3_stream_response::key={key}, bucket={settings.AWS_STORAGE_WEB_BUCKET_NAME}")
            s3_obj = s3_client.get_object(
                Bucket=settings.AWS_STORAGE_WEB_BUCKET_NAME,
                Key=key,
            )
            body = s3_obj['Body'].read()
            content_type = s3_obj.get('ContentType') or 'application/octet-stream'
            return HttpResponse(body, content_type=content_type, status=status_code)
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
        if file_path:
            response = self.get_s3_stream_response(s3_client, file_path)
            if response:
                return response

        splited_path = os.path.splitext(file_path)
        if not splited_path[1]:
            response = self.get_s3_stream_response(s3_client, os.path.join(file_path, "index.html"))
            if response:
                return response
        response = self.get_s3_stream_response(s3_client, '404.html', 404)
        if response:
            return response

        return defaults.page_not_found(request, self.kwargs.get('exception', None))


page_not_found_handler = cache_page(60 * 15)(PolaWebView.as_view())
