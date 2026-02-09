"""
Local settings

- Run in Debug mode
- Use console backend for emails
- Add Django Debug Toolbar
- Add django-extensions as app
"""

# pylint: disable=unused-wildcard-import

import environ

from .tests import *  # noqa: F403

env = environ.Env()

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG  # noqa: F405

ALLOWED_HOSTS = ['0.0.0.0', 'localhost', 'web', '127.0.0.1', '172.18.0.1', '172.18.0.2']
CSRF_TRUSTED_ORIGINS = [f"http://{host}:8080" for host in ALLOWED_HOSTS]

# django-debug-toolbar
# ------------------------------------------------------------------------------
MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)  # noqa: F405
INSTALLED_APPS += ('debug_toolbar',)  # noqa: F405

INTERNAL_IPS = ['127.0.0.1', '10.0.2.2', '192.168.99.1', '192.168.0.1', '0.0.0.0']

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': ['debug_toolbar.panels.redirects.RedirectsPanel'],
    'SHOW_TEMPLATE_CONTEXT': True,
    # 'SHOW_TOOLBAR_CALLBACK': lambda request: True
}

# Optional: override base URL for local GCS emulator/proxy.
GCS_PUBLIC_BASE_URL = env.str('POLA_APP_GCS_PUBLIC_BASE_URL', default='https://storage.googleapis.com')

# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += ()

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Your local stuff: Below this line define 3rd party library settings
MIDDLEWARE += ('pola.middlewares.SetHostToLocalhost',)
USE_X_FORWARDED_HOST = True

AI_SHARED_SECRET = env('AI_SHARED_SECRET', default='')
USE_ESCAPED_GCS_PATHS = True
USE_GCS_STORAGE = env.bool("USE_GCS_STORAGE", default=True)

if not USE_GCS_STORAGE:
    # Fallback mode for local runs without emulator.
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
