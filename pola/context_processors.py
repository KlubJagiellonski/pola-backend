from django.conf import settings


def app_settings(request):
    """
    Expose selected settings to templates.

    - IS_PRODUCTION: environment flag to detect production deployments
    - CMS_STATS_EXTERNAL_URL: external stats URL for production
    """
    return {
        'IS_PRODUCTION': getattr(settings, 'IS_PRODUCTION', False),
        'CMS_STATS_EXTERNAL_URL': getattr(settings, 'CMS_STATS_EXTERNAL_URL', ''),
    }
