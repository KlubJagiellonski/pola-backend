from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path, re_path
from django.views.defaults import (
    bad_request,
    page_not_found,
    permission_denied,
    server_error,
)
from django.views.generic import TemplateView

from pola import views_pola_web
from pola.views import (
    AdminStatsPageView,
    EditorsStatsPageView,
    FrontPageView,
    ReleaseView,
    StatsPageView,
)

urlpatterns = []
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
    path('release/', ReleaseView.as_view(), name="release"),
    path('cms/', FrontPageView.as_view(), name="home-cms"),
    path('cms/stats', StatsPageView.as_view(), name="home-stats"),
    path('cms/editors-stats', EditorsStatsPageView.as_view(), name="home-editors-stats"),
    path('cms/admin-stats', AdminStatsPageView.as_view(), name="home-admin-stats"),
    path(
        'cms/lang/',
        login_required(TemplateView.as_view(template_name='pages/lang-cms.html')),
        name="select_lang",
    ),
    re_path(r'^cms/product/', ('pola.product.urls', 'product', 'product')),
    re_path(r'^cms/company/', ('pola.company.urls', 'company', 'company')),
    re_path(r'^cms/report/', ('pola.report.urls', 'report', 'report')),
    re_path(r'^cms/ai_pics/', ('pola.ai_pics.urls', 'ai_pics', 'ai_pics')),
    re_path(r'^cms/gpc/', ('pola.gpc.urls', 'gpc', 'gpc')),
    re_path(r'^cms/concurency/', ('pola.concurency.urls', 'pola.concurency', 'concurency')),
]

# Debug stuff
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path('400/', bad_request, kwargs={'exception': Exception("Bad request")}),
        path('403/', permission_denied, kwargs={'exception': Exception("Permission Denied")}),
        path('404/', page_not_found, kwargs={'exception': Exception("Page not found")}),
        path('500/', server_error),
    ]

# All unknown URls fallback to S#
urlpatterns += [re_path('^.*', views_pola_web.page_not_found_handler)]
