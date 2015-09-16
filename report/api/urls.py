# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views
urlpatterns = [
    # url(regexp=r'/$',
    #     view=views.snippet_list),
    url(regex=r'report/attachment/$',
        view=views.AttachmentCreate.as_view()),
    url(regex=r'report/$',
        view=views.ReportCreate.as_view()),
]
