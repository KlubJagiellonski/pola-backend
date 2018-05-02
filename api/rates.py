from django.conf import settings


def whitelist(default):
    def rate(group, request):
        ip = request.META.get('REMOTE_ADDR')
        if ip in settings.WHITELIST_API_IP_ADDRESS:
            return None
        return default

    return rate
