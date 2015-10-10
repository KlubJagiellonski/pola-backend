# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(regex=r'get_by_code/(?P<code>[0-9]+)$',
        view=views.get_by_code,
        name="get_by_code"),
    url(
        regex=r'create$',
        view=views.ProductCreate.as_view(),
        name="create"),
    url(
        regex=r'(?P<code>[-\w]+)/image$',
        view=views.get_image,
        name="image"),
    url(
        regex=r'(?P<slug>[-\w]+)/edit$',
        view=views.ProductUpdate.as_view(),
        name="edit"),
    url(
        regex=r'(?P<slug>[-\w]+)/delete$',
        view=views.ProductDelete.as_view(),
        name="delete"),
    url(
        regex=r'(?P<slug>[-\w]+)/history$',
        view=views.ProductHistoryView.as_view(),
        name="view-history"),
    url(regex=r'(?P<slug>[-\w]+)/$',
        view=views.ProductDetailView.as_view(),
        name="detail"),
    url(regex=r'$',
        view=views.ProductListView.as_view(),
        name="list"),
]
