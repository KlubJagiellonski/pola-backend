import secrets
from typing import Optional

from django.conf import settings
from django.http import HttpResponse, JsonResponse


def require_static_bearer_token(request) -> Optional[HttpResponse]:
    """Validate Authorization: Bearer <token> against a static token from settings.

    - Reads token from settings.SET_BEARER_TOKEN configured via env var
      POLA_APP_SET_BEARER_TOKEN.
    - If the setting is empty/None, auth is not enforced (noop) to avoid
      breaking local/dev environments without configuration.
    - Returns None when authorized, or an HttpResponse (401) when unauthorized.
    """
    expected = getattr(settings, "SET_BEARER_TOKEN", None)
    if not expected:
        # No token configured -> do not enforce auth.
        return None

    auth_header = request.META.get("HTTP_AUTHORIZATION", "")
    if not auth_header.startswith("Bearer "):
        resp = JsonResponse({"detail": "Unauthorized"}, status=401)
        resp["WWW-Authenticate"] = "Bearer"
        return resp

    provided = auth_header[len("Bearer ") :].strip()
    if not secrets.compare_digest(provided, expected):
        resp = JsonResponse({"detail": "Unauthorized"}, status=401)
        resp["WWW-Authenticate"] = "Bearer error=\"invalid_token\""
        return resp

    return None
