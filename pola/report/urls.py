from django.urls import path, re_path

from . import views

urlpatterns = [
    path('advanced/', views.ReportAdvancedListView.as_view(), name="advanced"),
    re_path(r'(?P<pk>[-\w]+)/delete$', views.ReportDeleteView.as_view(), name="delete"),
    re_path(r'(?P<pk>[-\w]+)/resolve/$', views.ReportResolveView.as_view(), name="resolve"),
    re_path(r'(?P<pk>[-\w]+)/resolve-all/$', views.ReportResolveAllView.as_view(), name="resolve-all"),
    re_path(r'(?P<pk>[-\w]+)/$', views.ReportDetailView.as_view(), name="detail"),
    path('', views.ReportListView.as_view(), name="list"),
]
