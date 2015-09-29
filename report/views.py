# Create your views here.
from django.core.urlresolvers import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django_filters.views import FilterView
from . import models
from .filters import ReportFilter


class ReportListView(FilterView):
    model = models.Report
    filterset_class = ReportFilter
    paginate_by = 25


class ReportDelete(DeleteView):
    model = models.Report
    success_url = reverse_lazy('report:list')


class ReportDetailView(DetailView):
    model = models.Report
