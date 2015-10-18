from django.conf import settings
from django.http import HttpResponsePermanentRedirect

# from https://github.com/MidwestCommunications/django-hostname-redirects/

def _get_redirect(new_hostname, request):
    new_location = '%s://%s%s' % (
        request.is_secure() and 'https' or 'http',
        new_hostname,
        request.get_full_path()
    )
    return HttpResponsePermanentRedirect(new_location)

class HostnameRedirectMiddleware(object):
    def process_request(self, request):
        server_name = request.META['HTTP_HOST']
        catchall = getattr(settings,
            'CATCHALL_REDIRECT_HOSTNAME', None)
        # if catchall hostname is set, verify that the current
        # hostname is valid, and redirect if not
        if catchall:
            if server_name != catchall:
                return _get_redirect(catchall, request)
        return None
