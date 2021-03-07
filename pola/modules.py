from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.utils.deprecation import MiddlewareMixin


class SetRemoteAddrFromForwardedFor(MiddlewareMixin):
    """
    Middleware that sets REMOTE_ADDR based on HTTP_X_FORWARDED_FOR, if the
    latter is set. This is useful if you're sitting behind a reverse proxy that
    causes each request's REMOTE_ADDR to be set to 127.0.0.1.
    Note that this does NOT validate HTTP_X_FORWARDED_FOR. If you're not behind
    a reverse proxy that sets HTTP_X_FORWARDED_FOR automatically, do not use
    this middleware. Anybody can spoof the value of HTTP_X_FORWARDED_FOR, and
    because this sets REMOTE_ADDR based on HTTP_X_FORWARDED_FOR, that means
    anybody can "fake" their IP address. Only use this when you can absolutely
    trust the value of HTTP_X_FORWARDED_FOR.
    """

    def process_request(self, request):
        try:
            real_ip = request.META['HTTP_X_FORWARDED_FOR']
        except KeyError:
            return None
        else:
            # HTTP_X_FORWARDED_FOR can be a comma-separated list of IPs. The
            # client's IP will be the first one.
            real_ip = real_ip.split(",")[-1].strip()
            request.META['REMOTE_ADDR'] = real_ip


def _get_redirect(new_hostname, request):
    new_location = f"{request.is_secure() and 'https' or 'http'}://{new_hostname}{request.get_full_path()}"
    return HttpResponsePermanentRedirect(new_location)


class HostnameRedirectMiddleware(MiddlewareMixin):
    def process_request(self, request):
        server_name = request.META['HTTP_HOST']
        catchall = getattr(settings, 'SECURE_SSL_HOST', None)
        # if catchall hostname is set, verify that the current
        # hostname is valid, and redirect if not
        if catchall:
            if server_name != catchall:
                return _get_redirect(catchall, request)
        return None
