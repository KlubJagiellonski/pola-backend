"""
Local settings

- Run in Debug mode
- Use console backend for emails
- Add Django Debug Toolbar
- Add django-extensions as app
"""

from .common import *  # noqa: F403

TEMPLATES[0]['OPTIONS']['debug'] = True  # noqa: F405

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env("DJANGO_SECRET_KEY", default='CHANGEME!!!')  # noqa: F405

# Mail settings
# ------------------------------------------------------------------------------
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')  # noqa: F405

# CACHING
# ------------------------------------------------------------------------------
CACHES = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache', 'LOCATION': ''}}

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Your local stuff: Below this line define 3rd party library settings
GCS_PUBLIC_BUCKET_NAME = env('DJANGO_GCS_PUBLIC_BUCKET_NAME', default='test-public-bucket')  # noqa: F405
GCS_BACKEND_BUCKET_NAME = env('DJANGO_GCS_BACKEND_BUCKET_NAME', default='test-backend-bucket')  # noqa: F405
GCS_AI_PICS_BUCKET_NAME = env('DJANGO_GCS_AI_PICS_BUCKET_NAME', default='test-ai-pics-bucket')  # noqa: F405
GCS_WEB_BUCKET_NAME = env('DJANGO_GCS_WEB_BUCKET_NAME', default='test-web-bucket')  # noqa: F405
GCS_COMPANY_LOGOTYPE_BUCKET_NAME = env(  # noqa: F405
    'DJANGO_GCS_COMPANY_LOGOTYPE_BUCKET_NAME', default='test-logos-bucket'
)

# Disable Rate Limit
WHITELIST_API_IP_ADDRESS = ['127.0.0.1']
USE_ESCAPED_GCS_PATHS = False
