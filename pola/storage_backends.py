from django.conf import settings
from django.contrib.staticfiles.storage import StaticFilesStorage
from django.core.files.storage import FileSystemStorage
from storages.backends.gcloud import GoogleCloudStorage

USE_GCS_STORAGE = getattr(settings, "USE_GCS_STORAGE", True)

if USE_GCS_STORAGE:

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

else:

    class PublicStaticStorage(StaticFilesStorage):
        location = settings.STATIC_ROOT
        base_url = f"{settings.GCS_PUBLIC_BASE_URL}/{settings.GCS_PUBLIC_BUCKET_NAME}/"

    class BackendMediaStorage(FileSystemStorage):
        location = settings.MEDIA_ROOT
        base_url = f"{settings.GCS_PUBLIC_BASE_URL}/{settings.GCS_BACKEND_BUCKET_NAME}/"

    class AiPicsStorage(FileSystemStorage):
        location = settings.MEDIA_ROOT
        base_url = f"{settings.GCS_PUBLIC_BASE_URL}/{settings.GCS_AI_PICS_BUCKET_NAME}/"

    class CompanyLogotypeStorage(FileSystemStorage):
        location = settings.MEDIA_ROOT
        base_url = f"{settings.GCS_PUBLIC_BASE_URL}/{settings.GCS_COMPANY_LOGOTYPE_BUCKET_NAME}/"
