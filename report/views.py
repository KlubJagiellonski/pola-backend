from django.core.urlresolvers import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django_filters.views import FilterView
from pola.views import ActionView
from braces.views import LoginRequiredMixin
from .models import Report
from .filters import ReportFilter


class ReportListView(LoginRequiredMixin, FilterView):
    model = Report
    filterset_class = ReportFilter
    paginate_by = 25
    queryset = Report.objects.prefetch_related('attachment_set').all()


class ReportDelete(LoginRequiredMixin, DeleteView):
    model = Report
    success_url = reverse_lazy('report:list')


class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report


class ReportResolveView(LoginRequiredMixin, ActionView):
    model = Report
    template_name_suffix = '_resolve'
    queryset = models.Report.objects.only_open().all()

    def action(self):
        self.object.resolve(self.request.user)

    def get_success_url(self):
        return self.object.get_absolute_url()
