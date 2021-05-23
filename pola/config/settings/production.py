"""
Production Configurations

- Use djangosecure
- Use Amazon's S3 for storing static files and uploaded media
- Use mailgun to send emails
- Use Redis on Heroku

"""
# pylint: disable=unused-wildcard-import

import os
from urllib import parse as urlparse

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .common import *  # noqa: F403

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Raises ImproperlyConfigured exception if DJANGO_SECRET_KEY not in os.environ
SECRET_KEY = env("DJANGO_SECRET_KEY")  # noqa: F405

# This ensures that Django will be able to detect a secure connection
# properly on Heroku.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURITY_MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'pola.middlewares.SetRemoteAddrFromForwardedFor',
    'pola.middlewares.HostnameRedirectMiddleware',
)

# Make sure djangosecure.middleware.SecurityMiddleware is listed first
MIDDLEWARE = SECURITY_MIDDLEWARE + MIDDLEWARE  # noqa: F405

# set this to 60 seconds and then to 518400 when you can prove it works
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)  # noqa: F405
SECURE_FRAME_DENY = env.bool("DJANGO_SECURE_FRAME_DENY", default=True)  # noqa: F405
SECURE_CONTENT_TYPE_NOSNIFF = env.bool("DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True)  # noqa: F405
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True

SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)  # noqa: F405
SECURE_SSL_HOST = env("DJANGO_SECURE_SSL_HOST", default=None)  # noqa: F405

# SITE CONFIGURATION
# ------------------------------------------------------------------------------
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.6/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["www.pola-app.pl", "pola-app.pl", "pola-staging.herokuapp.com"]
# END SITE CONFIGURATION

INSTALLED_APPS += ("gunicorn",)  # noqa: F405

# See: https://github.com/antonagestam/collectfast
# For Django 1.7+, 'collectfast' should come before
# 'django.contrib.staticfiles'
AWS_PRELOAD_METADATA = True
COLLECTFAST_STRATEGY = "collectfast.strategies.boto3.Boto3Strategy"
COLLECTFAST_THREADS = 20

INSTALLED_APPS = ('collectfast',) + INSTALLED_APPS  # noqa: F405

# EMAIL
# ------------------------------------------------------------------------------
DEFAULT_FROM_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL')  # noqa: F405
ANYMAIL = {
    "MAILGUN_API_KEY": env('DJANGO_MAILGUN_API_KEY'),  # noqa: F405
    "MAILGUN_API_URL": "https://api.eu.mailgun.net/v3",  # noqa: F405
    "MAILGUN_SENDER_DOMAIN": env('DJANGO_MAILGUN_SERVER_NAME'),  # noqa: F405
}
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
EMAIL_SUBJECT_PREFIX = ''
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See:
# https://docs.djangoproject.com/en/dev/ref/templates/api/#django.template.loaders.cached.Loader
TEMPLATES[0]['OPTIONS']['loaders'] = [  # noqa: F405
    (
        'django.template.loaders.cached.Loader',
        ['django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader'],
    ),
]

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
DATABASES['default'] = env.db("DATABASE_URL")  # noqa: F405

# CACHING
# ------------------------------------------------------------------------------
redis_url = urlparse.urlparse(os.environ.get('REDISTOGO_URL', 'redis://localhost:6959'))

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': f'{redis_url.hostname}:{redis_url.port}',
        'OPTIONS': {'DB': 0, 'PASSWORD': redis_url.password},
    }
}

# Your production stuff: Below this line define 3rd party library settings


sentry_sdk.init(
    integrations=[DjangoIntegration()],
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
    dsn=env.str('SENTRY_DSN'),  # noqa: F405
    release=env.str('RELEASE_SHA'),  # noqa: F405
    traces_sample_rate=env.float('SENTRY_TRACES_SAMPLE_RATE', default=0),  # noqa: F405
)
