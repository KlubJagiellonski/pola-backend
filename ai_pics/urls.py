# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'$', views.AIPicsPageView.as_view(), name="list"),
]
