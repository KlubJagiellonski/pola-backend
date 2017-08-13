# Create your views here.
from braces.views import FormValidMessageMixin
from dal import autocomplete
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, QueryDict
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django_filters.views import FilterView

from company.models import Company
from pola.concurency import ConcurencyProtectUpdateView
from pola.views import ExprAutocompleteMixin
from report.models import Report
from .filters import CompanyFilter
from .forms import CompanyCreateFromKRSForm, CompanyForm


class CompanyListView(LoginRequiredMixin, FilterView):
    model = Company
    filterset_class = CompanyFilter
    paginate_by = 25


class GetInitalFormMixin(object):
    def get_initial(self):
        initials = super(GetInitalFormMixin, self).get_initial()
        initials.update(self.request.GET.dict())
        return initials


class CompanyCreate(GetInitalFormMixin,
                    LoginRequiredMixin,
                    FormValidMessageMixin,
                    CreateView):
    model = Company
    form_class = CompanyForm
    form_valid_message = u"Firma utworzona!"


class CompanyCreateFromKRSView(LoginRequiredMixin, FormView):
    form_class = CompanyCreateFromKRSForm
    template_name = 'company/company_from_krs.html'

    def form_valid(self, form, *args, **kwargs):
        company = form.cleaned_data['company']
        q = QueryDict('', mutable=True)
        q['official_name'] = company['nazwa']
        q['common_name'] = company['nazwa_skrocona']
        q['sources'] = u"Dane z KRS|%s" % company['url']
        q['nip'] = company['nip']
        q['address'] = company['adres']

        return HttpResponseRedirect(reverse('company:create') + '?' + q.urlencode())


class CompanyUpdate(LoginRequiredMixin,
                    FormValidMessageMixin,
                    ConcurencyProtectUpdateView,
                    UpdateView):
    model = Company
    form_class = CompanyForm
    concurency_url = reverse_lazy('concurency:lock')
    form_valid_message = u"Firma zaktualizowana!"


class CompanyDelete(LoginRequiredMixin,
                    FormValidMessageMixin,
                    DeleteView):
    model = Company
    success_url = reverse_lazy('company:list')
    form_valid_message = u"Firma skasowana!"


class FieldsDisplayMixin(object):
    def get_context_data(self, **kwargs):
        context = super(FieldsDisplayMixin, self).get_context_data(**kwargs)
        fields = []
        obj = self.get_object()
        for field_name in self.fields_to_display:
            try:
                method_display = getattr(
                    obj, 'get_' + field_name + '_display')
                value = method_display()
            except:
                value = obj.__dict__[field_name]
            fields.append(
                {"name": self.model._meta
                    .get_field(field_name).verbose_name,
                 "value": value})

        context['fields'] = fields
        return context


class CompanyDetailView(FieldsDisplayMixin, LoginRequiredMixin, DetailView):
    model = Company

    fields_to_display = (
        'Editor_notes',
        'name',
        'official_name',
        'common_name',
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
    )

    def get_context_data(self, **kwargs):
        context = super(CompanyDetailView, self).get_context_data(**kwargs)

        context['report_list'] = Report.objects.filter(
            product__company=self.get_object(), resolved_at=None)

        return context


class CompanyAutocomplete(LoginRequiredMixin, ExprAutocompleteMixin,
                          autocomplete.Select2QuerySetView):
    search_expr = [
        'name__icontains',
        'official_name__icontains',
        'common_name__icontains',
    ]
    model = Company
