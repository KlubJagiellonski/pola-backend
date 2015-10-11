from django.conf.urls import url
from . import views


urlpatterns = [
    url(regex=r'get_by_code/(?P<code>[0-9]+)$',
        view=views.get_by_code,
        name="get_by_code"),
]