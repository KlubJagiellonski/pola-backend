from django.conf.urls import url
from . import views


urlpatterns = [
    # API v2
    url(regex=r'v2/get_by_code$', view=views.get_by_code_v2,
        name="get_by_code_v2"),
    url(regex=r'v2/create_report$', view=views.create_report_v2,
        name="create_report_v2"),
    url(regex=r'v2/update_report$', view=views.update_report,
        name="update_report"),
    url(regex=r'v2/attach_file$', view=views.attach_file_v2,
        name="attach_file_v2"),

    # API v1
    url(regex=r'get_by_code/(?P<code>[0-9]+)$',
        view=views.get_by_code,
        name="get_by_code"),
    url(regex=r'create_report$', view=views.create_report,
        name="create_report"),
    url(regex=r'update_report$', view=views.update_report,
        name="update_report"),
    url(regex=r'attach_file$', view=views.attach_file,
        name="attach_file"),
]
