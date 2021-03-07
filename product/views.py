from braces.views import FormValidMessageMixin, MessageMixin
from dal import autocomplete
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import cache_page
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    DeleteView,
    FormView,
    UpdateView,
)
from django_filters.views import FilterView
from reportlab.graphics import renderPM
from reversion.models import Version

from pola.concurency import ConcurencyProtectUpdateView
from pola.mixins import LoginPermissionRequiredMixin
from pola.views import ExprAutocompleteMixin
from product.models import Product
from report.models import Report

from . import models
from .filters import ProductFilter
from .forms import AddBulkProductForm, ProductForm
from .images import Barcode


class ProductDetailView(LoginPermissionRequiredMixin, DetailView):
    permission_required = 'product.view_product'
    slug_field = 'code'
    model = models.Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = context['object']

        context['report_list'] = Report.objects.filter(product=obj, resolved_at=None)

        return context


class ProductListView(LoginPermissionRequiredMixin, FilterView):
    permission_required = 'product.view_product'
    model = models.Product
    filterset_class = ProductFilter
    paginate_by = 25


class ProductCreate(LoginPermissionRequiredMixin, FormValidMessageMixin, CreateView):
    permission_required = 'product.add_product'
    slug_field = 'code'
    model = models.Product
    form_class = ProductForm
    form_valid_message = _("Product created!")


class ProductUpdate(LoginPermissionRequiredMixin, ConcurencyProtectUpdateView, FormValidMessageMixin, UpdateView):
    permission_required = 'product.change_product'
    slug_field = 'code'
    model = models.Product
    form_class = ProductForm
    concurency_url = reverse_lazy('concurency:lock')
    form_valid_message = _("Produkt zaktualizowany!")


class ProductDelete(LoginPermissionRequiredMixin, FormValidMessageMixin, DeleteView):
    permission_required = 'product.delete_product'
    slug_field = 'code'
    model = models.Product
    success_url = reverse_lazy('product:list')
    form_valid_message = _("Product deleted!")


class ProductHistoryView(LoginPermissionRequiredMixin, DetailView):
    permission_required = 'product.view_product'
    slug_field = 'code'
    model = models.Product
    template_name = 'product/product_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['revision_list'] = Version.objects.get_for_object(self.get_object())
        return context


@cache_page(0)
def get_image(request, code):
    response = HttpResponse(content_type="image/png")
    barcode = Barcode.get_barcode(value=code, width=250)
    data = renderPM.drawToString(barcode, fmt='PNG')
    response.write(data)
    return response


class ProductAutocomplete(LoginRequiredMixin, ExprAutocompleteMixin, autocomplete.Select2QuerySetView):
    search_expr = [
        'name__icontains',
        'company__name__icontains',
        'company__official_name__icontains',
        'company__common_name__icontains',
    ]
    model = Product


class ProductBulkCreate(LoginPermissionRequiredMixin, MessageMixin, FormView):
    permission_required = 'product.add_product'
    form_class = AddBulkProductForm
    form_valid_message = _("Products created!")
    template_name = 'product/product_form.html'

    def form_valid(self, form):
        success, failed = form.save()
        msg = ""
        if success:
            msg += f"Zapisano {len(success)} produktów,\n"
            self.messages.success(msg, fail_silently=True)

        if failed:
            msg += f"Nie udało się zapisać {len(failed)} produktów.\n"
            msg += "Niepowodzenia: " + ",".join(f"{p} ({p.code})" for p in failed)
            self.messages.error(msg, fail_silently=True)

        return HttpResponseRedirect(form.cleaned_data['company'].get_absolute_url())
