# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'list$', views.BrandListView.as_view(), name="list"),
    url(r'$', views.search, name="search"),
]
