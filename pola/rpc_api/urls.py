from django.conf.urls import url

from . import views

urlpatterns = [
    # API v4
    url(regex=r'v4/get_by_code$', view=views.get_by_code_v4, name="get_by_code_v4"),
    url(regex=r'v4/create_report$', view=views.create_report_v3, name="create_report_v4"),
    url(regex=r'v4/update_report$', view=views.update_report_v2, name="update_report_v4"),
    # API v3
    url(regex=r'v3/add_ai_pics$', view=views.add_ai_pics, name="add_ai_pics"),
    url(regex=r'v3/get_by_code$', view=views.get_by_code_v3, name="get_by_code_v3"),
    url(regex=r'v3/create_report$', view=views.create_report_v3, name="create_report_v3"),
    url(regex=r'v3/update_report$', view=views.update_report_v2, name="update_report_v3"),
    # API v2
    url(regex=r'v2/get_by_code$', view=views.get_by_code_v2, name="get_by_code_v2"),
    url(regex=r'v2/create_report$', view=views.create_report_v2, name="create_report_v2"),
    url(regex=r'v2/update_report$', view=views.update_report_v2, name="update_report_v2"),
    url(regex=r'v2/attach_file$', view=views.attach_file_v2, name="attach_file_v2"),
    # Debug stuff
    url(regex=r"^PrTy9Df7k3hCeRW-raise-exception", view=views.raise_exception, name="raise_exception"),
]
