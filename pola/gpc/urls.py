from django.conf.urls import url

from . import views

urlpatterns = [
    # GPC Brick
    url(regex=r'gpc-brick/$', view=views.GPCBrickListView.as_view(), name="brick-list"),
    url(regex=r'gpc-brick/(?P<slug>[-\w]+)/$', view=views.GPCBrickDetailView.as_view(), name="brick-detail"),
    url(regex=r'gpc-brick/(?P<slug>[-\w]+)/edit$', view=views.GPCBrickUpdateView.as_view(), name="brick-edit"),
    # GPC Class
    url(regex=r'gpc-class/$', view=views.GPCClassListView.as_view(), name="class-list"),
    url(regex=r'gpc-class/(?P<slug>[-\w]+)/$', view=views.GPCClassDetailView.as_view(), name="class-detail"),
    url(regex=r'gpc-class/(?P<slug>[-\w]+)/edit$', view=views.GPCClassUpdateView.as_view(), name="class-edit"),
    # GPC Family
    url(regex=r'gpc-family/$', view=views.GPCFamilyListView.as_view(), name="family-list"),
    url(regex=r'gpc-family/(?P<slug>[-\w]+)/$', view=views.GPCFamilyDetailView.as_view(), name="family-detail"),
    url(regex=r'gpc-family/(?P<slug>[-\w]+)/edit$', view=views.GPCFamilyUpdateView.as_view(), name="family-edit"),
    # GPC Segment
    url(regex=r'gpc-segment/$', view=views.GPCSegmentListView.as_view(), name="segment-list"),
    url(regex=r'gpc-segment/(?P<slug>[-\w]+)/$', view=views.GPCSegmentDetailView.as_view(), name="segment-detail"),
    url(regex=r'gpc-segment/(?P<slug>[-\w]+)/edit$', view=views.GPCSegmentUpdateView.as_view(), name="segment-edit"),
]
