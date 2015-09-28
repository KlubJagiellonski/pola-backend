# -*- coding: utf-8 -*-

from product.api.views import ProductViewSet
from report.api.views import ReportViewSet, AttachmentViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'product', ProductViewSet)
router.register(r'report', ReportViewSet)
router.register(r'attachment', AttachmentViewSet)

urlpatterns = router.urls
