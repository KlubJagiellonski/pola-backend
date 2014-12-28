from api import views
from django.conf.urls import patterns, url

__author__ = 'paweljaneczek'


urlpatterns = patterns('',
    url(r'^product/(?P<barcode>\d+)/$', views.product, name='detail'),
)