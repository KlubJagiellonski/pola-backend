from django.conf import settings
from storages.backends.gcloud import GoogleCloudStorage


class PublicStaticStorage(GoogleCloudStorage):
    bucket_name = settings.GCS_PUBLIC_BUCKET_NAME
    default_acl = None
    querystring_auth = False


class BackendMediaStorage(GoogleCloudStorage):
    bucket_name = settings.GCS_BACKEND_BUCKET_NAME
    default_acl = None
    querystring_auth = True


class AiPicsStorage(GoogleCloudStorage):
    bucket_name = settings.GCS_AI_PICS_BUCKET_NAME
    default_acl = None
    querystring_auth = True


class CompanyLogotypeStorage(GoogleCloudStorage):
    bucket_name = settings.GCS_COMPANY_LOGOTYPE_BUCKET_NAME
    default_acl = None
    querystring_auth = False
