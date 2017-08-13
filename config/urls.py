# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.defaults import bad_request, permission_denied, page_not_found, server_error
from django.views.generic import TemplateView, RedirectView
from django.views.static import serve

from pola.views import FrontPageView, StatsPageView, EditorsStatsPageView, AdminStatsPageView, \
    AIPicsPageView

urlpatterns = [
    url(r'^$',
        TemplateView.as_view(template_name='index.html'), name="home"),
    url(r'^cms/$', FrontPageView.as_view(), name="home-cms"),
    url(r'^cms/stats$', StatsPageView.as_view(), name="home-stats"),
    url(r'^cms/editors-stats$', EditorsStatsPageView.as_view(), name="home-editors-stats"),
    url(r'^cms/admin-stats$', AdminStatsPageView.as_view(), name="home-admin-stats"),
    url(r'^cms/ai-pics$', AIPicsPageView.as_view(), name="home-ai-pics"),
    url(r'^cms/lang/$', login_required(
        TemplateView.as_view(template_name='pages/lang-cms.html')),
        name="select_lang"),
    url(r'^about/$',
        TemplateView.as_view(template_name='pages/about.html'), name="about"),

    url(r'^cms/product/', ('product.urls', 'product', 'product')),
    url(r'^cms/company/', ('company.urls', 'company', 'company')),
    url(r'^cms/report/', ('report.urls', 'report', 'report')),

    url(r'^grappelli/', include('grappelli.urls')),  # grappelli URLS
    url(r'^admin/', admin.site.urls),

    # User management
    url(r'^users/', ('pola.users.urls', 'pola.users', 'users')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),

    # url(r'^api/', include('pola.api.urls', namespace='api')),
    url(r'^a/', ('api.urls', 'api', 'api')),
    url(r'^m/', ('webviews.urls', 'webviews', 'webviews')),
    url(r'^concurency/', ('pola.concurency.urls', 'pola.concurency', 'concurency')),

    url(r'^robots\.txt$', TemplateView.as_view(
        template_name="robots.txt" if settings.IS_PRODUCTION
        else "robots-staging.txt", content_type='text/plain')),
]

FAVICON_FILES = [
    "favicon.ico",
    "apple-touch-icon.png",
    "apple-touch-icon-57x57.png",
    "apple-touch-icon-60x60.png",
    "apple-touch-icon-72x72.png",
    "apple-touch-icon-76x76.png",
    "apple-touch-icon-114x114.png",
    "apple-touch-icon-120x120.png",
    "apple-touch-icon-144x144.png",
    "apple-touch-icon-152x152.png",
    "apple-touch-icon-152x152.png",
    "apple-touch-icon-180x180.png",
    "browserconfig.xml",
]

for filename in FAVICON_FILES:
    urlpatterns.append(url(r'^' + filename + '$', RedirectView.as_view(
        url=settings.STATIC_URL + 'favicons/' + filename, permanent=True)))

# serving static files
urlpatterns += [
    url(r'^static/(?P<path>.*)$',
         serve, {'document_root': settings.STATIC_ROOT}),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', bad_request),
        url(r'^403/$', permission_denied),
        url(r'^404/$', page_not_found),
        url(r'^500/$', server_error),
    ]
