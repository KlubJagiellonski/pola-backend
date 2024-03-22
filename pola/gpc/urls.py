from django.urls import path, re_path

from . import views

urlpatterns = [
    # GPC Brick
    path('gpc-brick/', view=views.GPCBrickListView.as_view(), name="brick-list"),
    re_path(r'gpc-brick/(?P<slug>[-\w]+)/$', view=views.GPCBrickDetailView.as_view(), name="brick-detail"),
    re_path(r'gpc-brick/(?P<slug>[-\w]+)/edit$', view=views.GPCBrickUpdateView.as_view(), name="brick-edit"),
    # GPC Class
    path('gpc-class/', view=views.GPCClassListView.as_view(), name="class-list"),
    re_path(r'gpc-class/(?P<slug>[-\w]+)/$', view=views.GPCClassDetailView.as_view(), name="class-detail"),
    re_path(r'gpc-class/(?P<slug>[-\w]+)/edit$', view=views.GPCClassUpdateView.as_view(), name="class-edit"),
    # GPC Family
    path('gpc-family/', view=views.GPCFamilyListView.as_view(), name="family-list"),
    re_path(r'gpc-family/(?P<slug>[-\w]+)/$', view=views.GPCFamilyDetailView.as_view(), name="family-detail"),
    re_path(r'gpc-family/(?P<slug>[-\w]+)/edit$', view=views.GPCFamilyUpdateView.as_view(), name="family-edit"),
    # GPC Segment
    path('gpc-segment/', view=views.GPCSegmentListView.as_view(), name="segment-list"),
    re_path(r'gpc-segment/(?P<slug>[-\w]+)/$', view=views.GPCSegmentDetailView.as_view(), name="segment-detail"),
    re_path(r'gpc-segment/(?P<slug>[-\w]+)/edit$', view=views.GPCSegmentUpdateView.as_view(), name="segment-edit"),
]
