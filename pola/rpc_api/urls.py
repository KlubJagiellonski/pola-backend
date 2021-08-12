from django.urls import path, re_path

from pola.rpc_api import views_debug, views_v2, views_v3, views_v4

urlpatterns = [
    # API v4
    path(route='v4/get_by_code', view=views_v4.get_by_code_v4, name="get_by_code_v4"),
    path(route='v4/search', view=views_v4.SearchV4ApiView.as_view(), name="search_v4"),
    re_path(route=r'v4/create_report$', view=views_v3.create_report_v3, name="create_report_v4"),
    re_path(route=r'v4/update_report$', view=views_v2.update_report_v2, name="update_report_v4"),
    # API v3
    re_path(route=r'v3/add_ai_pics$', view=views_v3.add_ai_pics, name="add_ai_pics"),
    re_path(route=r'v3/get_by_code$', view=views_v3.get_by_code_v3, name="get_by_code_v3"),
    re_path(route=r'v3/create_report$', view=views_v3.create_report_v3, name="create_report_v3"),
    re_path(route=r'v3/update_report$', view=views_v2.update_report_v2, name="update_report_v3"),
    # API v2
    re_path(route=r'v2/get_by_code$', view=views_v2.get_by_code_v2, name="get_by_code_v2"),
    re_path(route=r'v2/create_report$', view=views_v2.create_report_v2, name="create_report_v2"),
    re_path(route=r'v2/update_report$', view=views_v2.update_report_v2, name="update_report_v2"),
    re_path(route=r'v2/attach_file$', view=views_v2.attach_file_v2, name="attach_file_v2"),
    # Debug stuff
    re_path(route=r"^PrTy9Df7k3hCeRW-raise-exception", view=views_debug.raise_exception, name="raise_exception"),
]
