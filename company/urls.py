# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'create$',
        views.CompanyCreate.as_view(), name="create"),
    url(r'create_from_krs$',
        views.CompanyCreateFromKRSView.as_view(), name="create_from_krs"),
    url(r'^company-autocomplete/$',
        views.CompanyAutocomplete.as_view(), name='company-autocomplete'),
    url(r'(?P<pk>[-\w]+)/edit$',
        views.CompanyUpdate.as_view(), name="edit"),
    url(r'(?P<pk>[-\w]+)/delete$',
        views.CompanyDelete.as_view(), name="delete"),
    # url(r'(?P<code>[-\w]+)/history$',
    #     views.CompanyHistoryView.as_view(), name="view-history"),
    url(r'(?P<pk>[-\w]+)/$',
        views.CompanyDetailView.as_view(), name="detail"),
    url(r'$',
        views.CompanyListView.as_view(), name="list"),
]
