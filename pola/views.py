from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.utils.encoding import force_text
from django.views.generic import TemplateView
from django.views.generic.detail import BaseDetailView, SingleObjectTemplateResponseMixin
from braces.views import LoginRequiredMixin
from company.models import Company
from product.models import Product
from report.models import Report


class FrontPageView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/home-cms.html'

    def get_context_data(self, *args, **kwargs):
        c = super(FrontPageView, self).get_context_data(**kwargs)
        c['oldest_reports'] = (Report.objects.only_open()
                                     .order_by('-created_at')[:10])
        c['newest_reports'] = (Report.objects.only_open()
                                     .order_by('created_at')[:10])
        c['most_popular_products'] = (Product.objects
                                             .with_query_count()
                                             .filter(company__isnull=True)
                                             .order_by('-query_count')[:10])
        c['most_popular_companies'] = (Company.objects
                                              .with_query_count()
                                              .filter(plCapital__isnull=True)
                                              .order_by('-query_count')[:10])
        return c


class ActionMixin(object):
    success_url = None

    def action(self):
        raise ImproperlyConfigured("No action to do. Provide a action body.")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.action()
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        if self.success_url:
            self.success_url = force_text(self.success_url)
            return self.success_url.format(**self.object.__dict__)
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")


class BaseActionView(ActionMixin, BaseDetailView):
    """
    Base view for action on an object.
    Using this base class requires subclassing to provide a response mixin.
    """


class ActionView(SingleObjectTemplateResponseMixin, BaseActionView):
    template_name_suffix = '_action'
