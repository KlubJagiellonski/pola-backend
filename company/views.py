# Create your views here.
from django.core.urlresolvers import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from . import models
from .filters import CompanyFilter
from .forms import ProductForm


class CompanyListView(FilterView):
    model = models.Company
    filterset_class = CompanyFilter

    def get_queryset(self, *args, **kwargs):
        qs = super(CompanyListView, self).get_queryset(*args, **kwargs)
        return qs.with_query_count()


class CompanyCreate(CreateView):
    model = models.Company
    form_class = ProductForm


class CompanyUpdate(UpdateView):
    model = models.Company
    form_class = ProductForm


class CompanyDelete(DeleteView):
    model = models.Company
    success_url = reverse_lazy('company:list')


class CompanyDetailView(DetailView):
    model = models.Company
