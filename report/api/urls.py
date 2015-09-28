# -*- coding: utf-8 -*-
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'report', views.ReportViewSet)
router.register(r'attachment', views.AttachmentViewSet)

urlpatterns = router.urls
