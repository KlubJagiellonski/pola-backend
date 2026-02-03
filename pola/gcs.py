import functools
from datetime import timedelta

from google.api_core import exceptions as gcs_exceptions
from google.cloud import storage


@functools.cache
def get_storage_client():
    return storage.Client()


@functools.cache
def get_bucket(bucket_name):
    return get_storage_client().bucket(bucket_name)


def fetch_blob(bucket_name, blob_name):
    blob = get_bucket(bucket_name).blob(blob_name)
    try:
        blob.reload()
    except gcs_exceptions.NotFound:
        return None
    return blob


def generate_signed_upload_url(bucket_name, object_name, content_type, expiration=timedelta(days=1)):
    blob = get_bucket(bucket_name).blob(object_name)
    return blob.generate_signed_url(
        version="v4",
        expiration=expiration,
        method="PUT",
        content_type=content_type,
    )
