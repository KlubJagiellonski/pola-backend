# Create your views here.
from django.core.urlresolvers import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from braces.views import LoginRequiredMixin
from report.models import Report
from company.models import Company
from .filters import CompanyFilter
from .forms import CompanyForm


class CompanyListView(LoginRequiredMixin, FilterView):
    model = Company
    filterset_class = CompanyFilter
    paginate_by = 25
    queryset = Company.objects.with_query_count().all()


class CompanyCreate(LoginRequiredMixin, CreateView):
    model = Company
    form_class = CompanyForm


class CompanyUpdate(LoginRequiredMixin, UpdateView):
    model = Company
    form_class = CompanyForm


class CompanyDelete(LoginRequiredMixin, DeleteView):
    model = Company
    success_url = reverse_lazy('company:list')

class CompanyDetailView(LoginRequiredMixin, DetailView):
    model = Company
    queryset = Company.objects.with_query_count().all()

    FIELDS_TO_DISPLAY = (
        'nip',
        'name',
        'official_name',
        'common_name',
        'address',
        'plCapital',
        'plCapital_notes',
        'plWorkers',
        'plWorkers_notes',
        'plRnD',
        'plRnD_notes',
        'plRegistered',
        'plRegistered_notes',
        'plNotGlobEnt',
        'plNotGlobEnt_notes',
        'verified',
    )

    def get_context_data(self, **kwargs):
        context = super(CompanyDetailView, self).get_context_data(**kwargs)

        context['report_list'] = Report.objects.filter(
            product__company=Company.objects.first())

        object = context['object']

        fields = []

        for field_name in self.FIELDS_TO_DISPLAY:
            try:
                method_display = getattr(object, 'get_'+field_name+'_display')
                value = method_display()
            except:
                value = object.__dict__[field_name]
            fields.append(
                {"name":self.model._meta.
                get_field_by_name(field_name)[0].verbose_name,
                "value":value})

        context['fields'] = fields
        return context
