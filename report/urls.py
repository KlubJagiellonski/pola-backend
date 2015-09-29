# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'(?P<pk>[-\w]+)/delete$',
        views.ReportDelete.as_view(), name="delete"),
    url(r'(?P<pk>[-\w]+)/resolve/$',
        views.ReportResolveView.as_view(), name="resolve"),
    url(r'(?P<pk>[-\w]+)/$',
        views.ReportDetailView.as_view(), name="detail"),
    url(r'$',
        views.ReportListView.as_view(), name="list"),
]
