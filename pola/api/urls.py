# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import url

from . import views


urlpatterns = [
    url(regex=r'obtain-token$',
        view=views.ObtainToken.as_view(),
        name="obtain-token"),
]

if settings.DEBUG:
    urlpatterns += [
        url(regex=r'test$',
            view=views.TestCredential.as_view(),
            name="test-credential"),
    ]
