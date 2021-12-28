from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'advanced/$', views.ReportAdvancedListView.as_view(), name="advanced"),
    url(r'(?P<pk>[-\w]+)/delete$', views.ReportDeleteView.as_view(), name="delete"),
    url(r'(?P<pk>[-\w]+)/resolve/$', views.ReportResolveView.as_view(), name="resolve"),
    url(r'(?P<pk>[-\w]+)/resolve-all/$', views.ReportResolveAllView.as_view(), name="resolve-all"),
    url(r'(?P<pk>[-\w]+)/$', views.ReportDetailView.as_view(), name="detail"),
    url(r'$', views.ReportListView.as_view(), name="list"),
]
