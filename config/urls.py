# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url, patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from pola.views import FrontPageView

urlpatterns = [
    url(r'^$',
        TemplateView.as_view(template_name='pages/home.html'), name="home"),
    url(r'^cms/$', FrontPageView.as_view(), name="home-cms"),
    url(r'^cms/lang/$',
        TemplateView.as_view(template_name='pages/lang-cms.html'), name="select_lang"),
    url(r'^about/$',
        TemplateView.as_view(template_name='pages/about.html'), name="about"),

    url(r'^cms/product/', include('product.urls', namespace='product')),
    url(r'^cms/company/', include('company.urls', namespace='company')),
    url(r'^cms/report/', include('report.urls', namespace='report')),

    url(r'^grappelli/', include('grappelli.urls')),  # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),

    # User management
    url(r'^users/', include("pola.users.urls", namespace="users")),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),

#    url(r'^api/', include('pola.api.urls', namespace='api')),
    url(r'^api/', include('api.urls', namespace='api')),

    url(r'^autocomplete/', include('autocomplete_light.urls'))
]

# serving static files
urlpatterns += patterns(
    '', (r'^static/(?P<path>.*)$',
         'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)

if settings.DEBUG:

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', 'django.views.defaults.bad_request'),
        url(r'^403/$', 'django.views.defaults.permission_denied'),
        url(r'^404/$', 'django.views.defaults.page_not_found'),
        url(r'^500/$', 'django.views.defaults.server_error'),
    ]
