from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path(r'create$', view=views.ProductCreate.as_view(), name="create"),
    re_path(r'create-bulk$', view=views.ProductBulkCreate.as_view(), name="create-bulk"),
    path('product-autocomplete/', views.ProductAutocomplete.as_view(), name='product-autocomplete'),
    re_path(r'(?P<code>[-\w]+)/image$', view=views.get_image, name="image"),
    re_path(r'(?P<slug>[-\w]+)/edit$', view=views.ProductUpdate.as_view(), name="edit"),
    re_path(r'(?P<slug>[-\w]+)/delete$', view=views.ProductDelete.as_view(), name="delete"),
    re_path(r'(?P<slug>[-\w]+)/history$', view=views.ProductHistoryView.as_view(), name="view-history"),
    re_path(r'(?P<slug>[-\w]+)/$', view=views.ProductDetailView.as_view(), name="detail"),
    path('', view=views.ProductListView.as_view(), name="list"),
]
