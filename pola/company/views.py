# Create your views here.
import typing

from braces.views import FormValidMessageMixin
from dal import autocomplete
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import HttpResponseRedirect, QueryDict
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    DeleteView,
    FormView,
    UpdateView,
)
from django_filters.views import FilterView

from pola.company.models import Brand, Company
from pola.concurency import ConcurencyProtectUpdateView
from pola.mixins import LoginPermissionRequiredMixin
from pola.product.models import Product
from pola.report.models import Report
from pola.views import ExprAutocompleteMixin

from ..logic_score import get_pl_score
from .filters import BrandFilter, CompanyFilter
from .forms import (
    BrandForm,
    BrandFormSet,
    BrandFormSetHelper,
    CompanyCreateFromKRSForm,
    CompanyForm,
)


class CompanyListView(LoginPermissionRequiredMixin, FilterView):
    permission_required = 'company.view_company'
    model = Company
    filterset_class = CompanyFilter
    paginate_by = 25


class GetInitalFormMixin:
    def get_initial(self):
        initials = super().get_initial()
        initials.update(self.request.GET.dict())
        return initials


class CompanyCreate(GetInitalFormMixin, LoginPermissionRequiredMixin, FormValidMessageMixin, CreateView):
    permission_required = 'company.add_company'
    model = Company
    form_class = CompanyForm
    form_valid_message = "Firma utworzona!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['brand_formset'] = BrandFormSet(self.request.POST)
        else:
            context['brand_formset'] = BrandFormSet()
        context['brand_formset_helper'] = BrandFormSetHelper()
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['brand_formset']
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)


class CompanyCreateFromKRSView(LoginPermissionRequiredMixin, FormView):
    permission_required = 'company.add_company'
    form_class = CompanyCreateFromKRSForm
    template_name = 'company/company_from_krs.html'

    def form_valid(self, form, *args, **kwargs):
        company = form.cleaned_data['company']
        q = QueryDict('', mutable=True)
        q['official_name'] = company['nazwa']
        q['common_name'] = company['nazwa_skrocona']
        q['sources'] = f"Dane z KRS|{company['url']}"
        q['nip'] = company['nip']
        q['address'] = company['adres']

        return HttpResponseRedirect(reverse('company:create') + '?' + q.urlencode())


class CompanyUpdate(LoginPermissionRequiredMixin, FormValidMessageMixin, ConcurencyProtectUpdateView, UpdateView):
    permission_required = 'company.change_company'
    model = Company
    form_class = CompanyForm
    concurency_url = reverse_lazy('concurency:lock')
    form_valid_message = "Firma zaktualizowana!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['brand_formset'] = BrandFormSet(self.request.POST, instance=self.object)
        else:
            context['brand_formset'] = BrandFormSet(instance=self.object)
        context['brand_formset_helper'] = BrandFormSetHelper()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        formset = BrandFormSet(self.request.POST, instance=self.object)
        if formset.is_valid():
            formset.save()
        else:
            return super().form_invalid(form)
        return response


class CompanyDelete(LoginPermissionRequiredMixin, FormValidMessageMixin, DeleteView):
    permission_required = 'company.delete_company'
    model = Company
    success_url = reverse_lazy('company:list')
    form_valid_message = "Firma skasowana!"


class FieldsDisplayMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields = []
        for field_name in self.fields_to_display:
            obj = self.get_object()
            name = self._lookup_field_info(
                obj,
                'get_' + field_name + '_display_name',
                default=lambda: self.model._meta.get_field(field_name).verbose_name,
            )

            value = self._lookup_field_info(
                obj, 'get_' + field_name + '_display', default=lambda: obj.__dict__[field_name]
            )

            fields.append({"name": name, "value": value})

        context['fields'] = fields
        return context

    def _lookup_field_info(self, obj, method_name, default=None):
        if hasattr(self, method_name):
            fn = getattr(self, method_name)
            return fn()

        if hasattr(obj, method_name):
            fn = getattr(obj, method_name)
            return fn()

        if default:
            if callable(default):
                return default()
            return default
        return None


class CompanyCardModel(typing.NamedTuple):
    pl_score: int
    pl_capital: int
    pl_workers: bool
    pl_rnd: bool
    pl_registered: bool
    pl_not_glob_ent: bool
    product_count: int
    product_query_count: int
    most_popular_code: str


class CompanyDetailView(FieldsDisplayMixin, LoginPermissionRequiredMixin, DetailView):
    model = Company
    permission_required = 'company.view_company'

    fields_to_display = (
        'Editor_notes',
        'name',
        'official_name',
        'common_name',
        'is_friend',
        'plCapital',
        'plWorkers',
        'plRnD',
        'plRegistered',
        'plNotGlobEnt',
        'description',
        'sources',
        'verified',
        'address',
        'nip',
        'logotype',
        'official_url',
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['report_list'] = Report.objects.only_open().filter(product__company=self.object)

        context['brand_list'] = Brand.objects.filter(company=self.object)
        context['product_list'] = Product.objects.filter(company=self.object).order_by('-query_count')

        if self.object.verified:
            context['company_card'] = CompanyCardModel(
                pl_score=get_pl_score(self.object),
                pl_capital=self.object.plCapital,
                pl_workers=self.object.plWorkers,
                pl_rnd=self.object.plRnD,
                pl_registered=self.object.plRegistered,
                pl_not_glob_ent=self.object.plNotGlobEnt,
                product_count=context['product_list'].count(),
                product_query_count=context['product_list'].aggregate(total=Sum('query_count'))['total'] or 0,
                most_popular_code=context['product_list'].first().code if context['product_list'] else None,
            )
        return context


class CompanyAutocomplete(LoginRequiredMixin, ExprAutocompleteMixin, autocomplete.Select2QuerySetView):
    search_expr = [
        'name__icontains',
        'official_name__icontains',
        'common_name__icontains',
    ]
    model = Company


class BrandListView(LoginPermissionRequiredMixin, FilterView):
    permission_required = 'company.view_company'
    model = Brand
    filterset_class = BrandFilter
    paginate_by = 25


class BrandCreate(GetInitalFormMixin, LoginPermissionRequiredMixin, FormValidMessageMixin, CreateView):
    permission_required = 'company.add_company'
    model = Brand
    form_class = BrandForm
    form_valid_message = "Marka utworzona!"

    def get_success_url(self):
        if self.object.company:
            return reverse("company:brand-detail", args=[self.object.company.pk])
        return reverse("company:brand-detail", args=[self.object.pk])


class BrandUpdate(LoginPermissionRequiredMixin, FormValidMessageMixin, ConcurencyProtectUpdateView, UpdateView):
    permission_required = 'company.change_company'
    model = Brand
    form_class = BrandForm
    concurency_url = reverse_lazy('concurency:lock')
    form_valid_message = "Marka zaktualizowana!"

    def get_success_url(self):
        if self.object.company:
            return reverse("company:detail", args=[self.object.company.pk])
        return reverse("company:brand-list")


class BrandDelete(LoginPermissionRequiredMixin, FormValidMessageMixin, DeleteView):
    permission_required = 'company.delete_company'
    model = Brand
    success_url = reverse_lazy('company:list')
    form_valid_message = "Marka skasowana!"

    def get_success_url(self):
        if self.object.company:
            return reverse("company:detail", args=[self.object.company.pk])
        return reverse("company:brand-list")


class BrandDetailView(FieldsDisplayMixin, LoginPermissionRequiredMixin, DetailView):
    model = Brand
    permission_required = 'company.view_company'

    fields_to_display = (
        'name',
        'common_name',
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['total_query_count'] = Product.objects.filter(brand=self.object).aggregate(total=Sum('query_count'))[
            'total'
        ]

        return context


class BrandAutocomplete(LoginRequiredMixin, ExprAutocompleteMixin, autocomplete.Select2QuerySetView):
    search_expr = [
        'name__icontains',
        'common_name__icontains',
    ]
    model = Brand
