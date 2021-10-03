from urllib.parse import urlparse

import boto3
from boto.s3.connection import OrdinaryCallingFormat, S3Connection
from botocore.config import Config
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


def create_s3_client():
    session = boto3.session.Session()

    if settings.AWS_S3_ENDPOINT_URL:
        return session.client(
            service_name='s3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            config=Config(signature_version='s3v4'),
            region_name='us-east-1',
        )

    return session.client(
        service_name='s3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name='us-east-1',
    )


def create_s3_resource():
    session = boto3.session.Session()

    if settings.AWS_S3_ENDPOINT_URL:
        return session.resource(
            service_name='s3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            config=Config(signature_version='s3v4'),
            region_name='us-east-1',
        )

    return session.resource(
        service_name='s3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name='us-east-1',
    )
