"""
Local settings

- Run in Debug mode
- Use console backend for emails
- Add Django Debug Toolbar
- Add django-extensions as app
"""

from .common import *  # noqa: F403
from .common import env

TEMPLATES[0]['OPTIONS']['debug'] = True  # noqa: F405

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env("DJANGO_SECRET_KEY", default='CHANGEME!!!')

# Mail settings
# ------------------------------------------------------------------------------
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')

# CACHING
# ------------------------------------------------------------------------------
CACHES = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache', 'LOCATION': ''}}

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Your local stuff: Below this line define 3rd party library settings
GCS_PUBLIC_BUCKET_NAME = env('DJANGO_GCS_PUBLIC_BUCKET_NAME', default='test-public-bucket')
GCS_BACKEND_BUCKET_NAME = env('DJANGO_GCS_BACKEND_BUCKET_NAME', default='test-backend-bucket')
GCS_AI_PICS_BUCKET_NAME = env('DJANGO_GCS_AI_PICS_BUCKET_NAME', default='test-ai-pics-bucket')
GCS_WEB_BUCKET_NAME = env('DJANGO_GCS_WEB_BUCKET_NAME', default='test-web-bucket')
GCS_COMPANY_LOGOTYPE_BUCKET_NAME = env(
    'DJANGO_GCS_COMPANY_LOGOTYPE_BUCKET_NAME', default='pola-app-company-logotype'
)
GCS_PUBLIC_BASE_URL = env.str('POLA_APP_GCS_PUBLIC_BASE_URL', default='http://127.0.0.1:8765')

# Disable Rate Limit
WHITELIST_API_IP_ADDRESS = ['127.0.0.1']
USE_ESCAPED_GCS_PATHS = False
USE_GCS_STORAGE = False

# Use local filesystem storage for tests to avoid GCS credentials.
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
