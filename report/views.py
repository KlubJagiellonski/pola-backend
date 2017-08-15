#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django_filters.views import FilterView

from pola.views import ActionView
from . import models
from .filters import ReportFilter


class ReportListView(LoginRequiredMixin, FilterView):
    model = models.Report
    filterset_class = ReportFilter
    paginate_by = 25
    queryset = models.Report.objects.all().prefetch_related('attachment_set')


class ReportAdvancedListView(LoginRequiredMixin, FilterView):
    model = models.Report
    filterset_class = ReportFilter
    paginate_by = 25
    template_name_suffix = '_filter_adv'
    queryset = models.Report.objects.all().prefetch_related('attachment_set')

    def post(self, request, *args, **kwargs):
        messages.success(request, "Raporty zostały rozpatrzone")
        ids = request.POST.getlist('report_to_resolve')
        models.Report.objects.filter(pk__in=ids).resolve(self.request.user)
        return HttpResponseRedirect(request.get_full_path())


class ReportDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Report
    success_url = reverse_lazy('report:list')


class ReportDetailView(LoginRequiredMixin, DetailView):
    model = models.Report


class ReportResolveView(LoginRequiredMixin, ActionView):
    model = models.Report
    template_name_suffix = '_resolve'
    queryset = models.Report.objects.only_open().all()

    def action(self):
        self.object.resolve(self.request.user)

    def get_success_url(self):
        return self.object.get_absolute_url()
