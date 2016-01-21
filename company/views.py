# Create your views here.
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, \
    ProcessFormView
from django_filters.views import FilterView
from braces.views import LoginRequiredMixin, FormValidMessageMixin
from report.models import Report
from company.models import Company
from pola.concurency import ConcurencyProtectUpdateView
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect, QueryDict
from .filters import CompanyFilter
from .forms import CompanyForm, CompanyCreateFromKRSForm


class CompanyListView(LoginRequiredMixin, FilterView):
    model = Company
    filterset_class = CompanyFilter
    paginate_by = 25
    queryset = Company.objects.with_query_count().all()


class CompanyCreate(LoginRequiredMixin,
                    FormValidMessageMixin,
                    CreateView):
    model = Company
    form_class = CompanyForm
    form_valid_message = u"Firma utworzona!"

    def get_initial(self):
        initials = {}
        for field_name in CompanyDetailView.FIELDS_TO_DISPLAY:
            initials[field_name]= self.request.GET.get(field_name)
        return initials

class CompanyCreateFromKRSView(LoginRequiredMixin, ProcessFormView):
    form_class = CompanyCreateFromKRSForm
    template_name = 'company/company_from_krs.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            company = form.cleaned_data['company']
            q = QueryDict(mutable=True)
            q['official_name'] = company['nazwa']
            q['common_name'] = company['nazwa_skrocona']
            q['sources'] = u"Dane z KRS|%s" % company['url']
            q['nip'] = company['nip']
            q['address'] = company['adres']

            return HttpResponseRedirect(u'/cms/company/create?'+q.urlencode())

        return render(request, self.template_name, {'form': form})


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


class CompanyDetailView(LoginRequiredMixin, DetailView):
    model = Company
    queryset = Company.objects.with_query_count().all()

    FIELDS_TO_DISPLAY = (
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

        object = context['object']

        context['report_list'] = Report.objects.filter(
            product__company=object, resolved_at=None)

        fields = []

        for field_name in self.FIELDS_TO_DISPLAY:
            try:
                method_display = getattr(object, 'get_'+field_name+'_display')
                value = method_display()
            except:
                value = object.__dict__[field_name]
            fields.append(
                {"name": self.model._meta
                    .get_field_by_name(field_name)[0].verbose_name,
                 "value": value})

        context['fields'] = fields
        return context
