from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from django.views.defaults import (
    bad_request,
    page_not_found,
    permission_denied,
    server_error,
)
from django.views.generic import RedirectView, TemplateView
from django.views.static import serve

from pola import views_pola_web
from pola.views import (
    AdminStatsPageView,
    EditorsStatsPageView,
    FrontPageView,
    StatsPageView,
)

urlpatterns = []
# Add static pages
if not settings.ENABLE_POLA_WEB_CUSTOMIZATION:
    urlpatterns += [
        re_path(r'^$', TemplateView.as_view(template_name='index.html'), name="home"),
        re_path(r'^friends$', TemplateView.as_view(template_name='friends.html'), name="friends"),
        re_path(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name="about"),
    ]
# Add mobile static pages
urlpatterns += [
    re_path(r'^m/', ('pola.webviews.urls', 'webviews', 'webviews')),
]
# Add RPC API
urlpatterns += [
    path('a/', ('pola.rpc_api.urls', 'api', 'api')),
]
# Add special BI views
urlpatterns += [
    path('bi-export/', ('pola.bi_export.urls', 'bi_export', 'bi_export')),
]
# Add system views
urlpatterns += [
    re_path(
        r'^robots\.txt$',
        TemplateView.as_view(
            template_name="robots.txt" if settings.IS_PRODUCTION else "robots-staging.txt",
            content_type='text/plain',
        ),
    ),
]
# Add Admin Views
urlpatterns += [
    re_path(r'^grappelli/', include('grappelli.urls')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^users/', ('pola.users.urls', 'pola.users', 'users')),
    re_path(r'^accounts/', include('allauth.urls')),
    re_path(r'^i18n/', include('django.conf.urls.i18n')),
]
# Add CMS views
urlpatterns += [
    re_path(r'^cms/$', FrontPageView.as_view(), name="home-cms"),
    re_path(r'^cms/stats$', StatsPageView.as_view(), name="home-stats"),
    re_path(r'^cms/editors-stats$', EditorsStatsPageView.as_view(), name="home-editors-stats"),
    re_path(r'^cms/admin-stats$', AdminStatsPageView.as_view(), name="home-admin-stats"),
    re_path(
        r'^cms/lang/$',
        login_required(TemplateView.as_view(template_name='pages/lang-cms.html')),
        name="select_lang",
    ),
    re_path(r'^cms/product/', ('product.urls', 'product', 'product')),
    re_path(r'^cms/company/', ('company.urls', 'company', 'company')),
    re_path(r'^cms/report/', ('report.urls', 'report', 'report')),
    re_path(r'^cms/ai_pics/', ('ai_pics.urls', 'ai_pics', 'ai_pics')),
    re_path(r'^cms/concurency/', ('pola.concurency.urls', 'pola.concurency', 'concurency')),
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

if not settings.ENABLE_POLA_WEB_CUSTOMIZATION:
    for filename in FAVICON_FILES:
        urlpatterns.append(
            url(
                rf'^{filename}$',
                RedirectView.as_view(url=f'{settings.STATIC_URL}favicons/{filename}', permanent=True),
            )
        )

# Serving static files
if not settings.ENABLE_POLA_WEB_CUSTOMIZATION:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', bad_request, kwargs={'exception': Exception("Bad request")}),
        url(r'^403/$', permission_denied, kwargs={'exception': Exception("Permission Denied")}),
        url(r'^404/$', page_not_found, kwargs={'exception': Exception("Page not found")}),
        url(r'^500/$', server_error),
    ]

if settings.ENABLE_POLA_WEB_CUSTOMIZATION:
    urlpatterns += [re_path('^.*', views_pola_web.page_not_found_handler)]
