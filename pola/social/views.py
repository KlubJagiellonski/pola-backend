import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import BaseFormView
from ratelimit.decorators import ratelimit

from pola.rpc_api.http import JsonProblemResponse
from pola.rpc_api.openapi import validate_pola_openapi_spec
from pola.rpc_api.rates import whitelist
from pola.social.forms import SubscribeNewsletterForm


@method_decorator(ratelimit(key='ip', rate=whitelist('2/s'), block=True), name='dispatch')
@method_decorator(validate_pola_openapi_spec, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class SubscribeNewsletterFormView(BaseFormView):
    form_class = SubscribeNewsletterForm

    def get(self, request, *args, **kwargs):
        return JsonProblemResponse(
            status=405, title="Metoda niedozwolona.", detail="Aby wysłać żadanie, musisz wysłać żadanie POST."
        )

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        if form.save():
            return HttpResponse(status=204)
        return JsonProblemResponse(status=500, title="Nie zapisano.", detail="Nie udało się zapisać formularza.")

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return JsonProblemResponse(
            status=400,
            title="Weryfikacja formularza nie powiodła się.",
            detail="Formularz zawiera błędy i nie można go zapisać.",
            context_data=form.errors.get_json_data(),
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        if self.request.method in ('POST', 'PUT'):
            kwargs['data'] = json.loads(self.request.body)

        return kwargs
