from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import TokenAuthentication
from ..models import Client


class ClientTokenAuthentication(TokenAuthentication):
    model = Client

    def authenticate_credentials(self, key):
        try:
            client = self.model.objects.get(token=key)
        except self.model.DoesNotExist:
            raise AuthenticationFailed(_('Invalid token.'))

        return (client, None)
