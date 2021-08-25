from django.urls import path

from pola.bi_export.views import ExportView

urlpatterns = [
    path(route='top_companies', view=ExportView.as_view(), name="top_companies"),
]
