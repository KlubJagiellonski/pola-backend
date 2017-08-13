from braces.views import FormValidMessageMixin
from dal import autocomplete
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import cache_page
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django_filters.views import FilterView
from reportlab.graphics import renderPM
from reversion.models import Version

from pola.concurency import ConcurencyProtectUpdateView
from pola.views import ExprAutocompleteMixin
from product.models import Product
from report.models import Report
from . import models
from .filters import ProductFilter
from .forms import ProductForm
from .images import Barcode


class ProductDetailView(LoginRequiredMixin, DetailView):
    slug_field = 'code'
    model = models.Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)

        obj = context['object']

        context['report_list'] = Report.objects.filter(
            product=obj, resolved_at=None)

        return context


class ProductListView(LoginRequiredMixin, FilterView):
    model = models.Product
    filterset_class = ProductFilter
    paginate_by = 25


class ProductCreate(LoginRequiredMixin, FormValidMessageMixin, CreateView):
    slug_field = 'code'
    model = models.Product
    form_class = ProductForm
    form_valid_message = _(u"Product created!")


class ProductUpdate(LoginRequiredMixin,
                    ConcurencyProtectUpdateView,
                    FormValidMessageMixin,
                    UpdateView):
    slug_field = 'code'
    model = models.Product
    form_class = ProductForm
    concurency_url = reverse_lazy('concurency:lock')
    form_valid_message = _(u"Produkt zaktualizowany!")


class ProductDelete(LoginRequiredMixin, FormValidMessageMixin, DeleteView):
    slug_field = 'code'
    model = models.Product
    success_url = reverse_lazy('product:list')
    form_valid_message = _(u"Product deleted!")


class ProductHistoryView(LoginRequiredMixin, DetailView):
    slug_field = 'code'
    model = models.Product
    template_name = 'product/product_history.html'

    def get_context_data(self, **kwargs):
        context = super(ProductHistoryView, self).get_context_data(**kwargs)
        context['revision_list'] = Version.objects.get_for_object(self.get_object())
        return context


@cache_page(0)
def get_image(request, code):
    response = HttpResponse(content_type="image/png")
    barcode = Barcode.get_barcode(value=code, width=250)
    data = renderPM.drawToString(barcode, fmt='PNG')
    response.write(data)
    return response


class ProductAutocomplete(LoginRequiredMixin, ExprAutocompleteMixin,
                          autocomplete.Select2QuerySetView):
    search_expr = [
        'name__icontains',
        'company__name__icontains',
        'company__official_name__icontains',
        'company__common_name__icontains',
    ]
    model = Product
