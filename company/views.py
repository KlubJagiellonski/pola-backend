# Create your views here.
from django.core.urlresolvers import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from braces.views import LoginRequiredMixin
from . import models
from .filters import CompanyFilter
from .forms import CompanyForm


class CompanyListView(LoginRequiredMixin, FilterView):
    model = models.Company
    filterset_class = CompanyFilter
    paginate_by = 25
    queryset = models.Company.objects.with_query_count().all()


class CompanyCreate(LoginRequiredMixin, CreateView):
    model = models.Company
    form_class = CompanyForm


class CompanyUpdate(LoginRequiredMixin, UpdateView):
    model = models.Company
    form_class = CompanyForm


class CompanyDelete(LoginRequiredMixin, DeleteView):
    model = models.Company
    success_url = reverse_lazy('company:list')


class CompanyDetailView(LoginRequiredMixin, DetailView):
    model = models.Company
    queryset = models.Company.objects.with_query_count().all()
