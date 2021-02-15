"""
Local settings

- Run in Debug mode
- Use console backend for emails
- Add Django Debug Toolbar
- Add django-extensions as app
"""
# pylint: disable=unused-wildcard-import

import os

from .tests import *  # noqa: F403

IS_DOCKER = os.path.exists('/.dockerenv')
# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)  # noqa: F405
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG  # noqa: F405

if IS_DOCKER:
    ALLOWED_HOSTS = ['0.0.0.0', 'localhost']

# django-debug-toolbar
# ------------------------------------------------------------------------------
MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)  # noqa: F405
INSTALLED_APPS += ('debug_toolbar',)  # noqa: F405

INTERNAL_IPS = ['127.0.0.1', '10.0.2.2', '192.168.99.1', '192.168.0.1']
if IS_DOCKER:
    INTERNAL_IPS.append('0.0.0.0')

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': ['debug_toolbar.panels.redirects.RedirectsPanel'],
    'SHOW_TEMPLATE_CONTEXT': True,
    # 'SHOW_TOOLBAR_CALLBACK': lambda request: True
}

# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += ('django_extensions',)  # noqa: F405

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Your local stuff: Below this line define 3rd party library settings
AI_SHARED_SECRET = env('AI_SHARED_SECRET', default='')  # noqa: F405
