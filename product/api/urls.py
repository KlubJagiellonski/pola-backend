# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views
urlpatterns = [
    # url(regexp=r'/$',
    #     view=views.snippet_list),
    url(regex=r'(?P<slug>[-\w]+)/$',
        view=views.ProductDetail.as_view()),
]
