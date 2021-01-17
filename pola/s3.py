from urllib.parse import urlparse

from boto.s3.connection import OrdinaryCallingFormat, S3Connection
from django.conf import settings


def create_s3_connection():
    if not settings.AWS_S3_ENDPOINT_URL:
        return S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
    url_parts = urlparse(settings.AWS_S3_ENDPOINT_URL)
    return S3Connection(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        is_secure=url_parts.scheme.lower() == 'https',
        host=url_parts.hostname,
        port=url_parts.port,
        calling_format=OrdinaryCallingFormat(),
    )
