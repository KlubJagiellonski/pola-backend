from django.urls import path

from . import views

urlpatterns = [
    path('', views.AIPicsPageView.as_view(), name="list"),
    path('<int:pk>', views.AIPicsDetailView.as_view(), name="detail"),
    path('api/set-api-pic-state', views.ApiSetAiPicStateView.as_view(), name='set-api-pic-state'),
    path('api/delete-api-pic', views.ApiDeleteAiPicsView.as_view(), name='delete-api-pic'),
    path('api/delete-attachment', views.ApiDeleteAttachmentView.as_view(), name='delete-attachment'),
]
