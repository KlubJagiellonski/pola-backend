# -*- coding: utf-8 -*-
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'product', views.ProductViewSet)

urlpatterns = router.urls
