from django.urls import path, re_path

from . import views

urlpatterns = [
    # URL pattern for the UserListView
    path('', view=views.UserListView.as_view(), name='list'),
    # URL pattern for the UserRedirectView
    path('~redirect/', view=views.UserRedirectView.as_view(), name='redirect'),
    # URL pattern for the UserDetailView
    re_path(r'^(?P<username>[\w.@+-]+)/$', view=views.UserDetailView.as_view(), name='detail'),
    # URL pattern for the UserUpdateView
    path(r'~update/', view=views.UserUpdateView.as_view(), name='update'),
]
