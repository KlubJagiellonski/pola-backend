import functools

import boto3
from botocore.config import Config
from django.conf import settings


def _s3_config():
    if settings.AWS_S3_ENDPOINT_URL:
        return Config(signature_version='s3v4', s3={'addressing_style': 'path'})
    return Config(signature_version='s3v4')


@functools.cache
def create_s3_client():
    session = boto3.session.Session()

    if settings.AWS_S3_ENDPOINT_URL:
        return session.client(
            service_name='s3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            config=_s3_config(),
            region_name='us-east-1',
        )

    return session.client(
        service_name='s3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name='us-east-1',
    )


@functools.cache
def create_s3_resource():
    session = boto3.session.Session()

    if settings.AWS_S3_ENDPOINT_URL:
        return session.resource(
            service_name='s3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            config=_s3_config(),
            region_name='us-east-1',
        )

    return session.resource(
        service_name='s3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name='us-east-1',
    )


def list_bucket_keys(bucket_name):
    s3_client = create_s3_client()
    paginator = s3_client.get_paginator('list_objects_v2')
    keys = set()
    for page in paginator.paginate(Bucket=bucket_name):
        for obj in page.get('Contents', []):
            keys.add(obj['Key'])
    return keys


def delete_bucket_key(bucket_name, key):
    create_s3_client().delete_object(Bucket=bucket_name, Key=key)
