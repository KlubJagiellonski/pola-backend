from django.urls import path

from . import views

urlpatterns = [
    # Comapny
    path('', views.CompanyListView.as_view(), name="list"),
    path('create', views.CompanyCreate.as_view(), name="create"),
    path('create_from_krs', views.CompanyCreateFromKRSView.as_view(), name="create_from_krs"),
    path('<int:pk>/edit', views.CompanyUpdate.as_view(), name="edit"),
    path('<int:pk>/delete', views.CompanyDelete.as_view(), name="delete"),
    # url(r'(?P<code>[-\w]+)/history$',
    #     views.CompanyHistoryView.as_view(), name="view-history"),
    path('<int:pk>', views.CompanyDetailView.as_view(), name="detail"),
    # Brand
    path('brand', views.BrandListView.as_view(), name="brand-list"),
    path('create-brand', views.BrandCreate.as_view(), name="brand-create"),
    path('brand/<int:pk>/edit', views.BrandUpdate.as_view(), name="brand-edit"),
    path('brand/<int:pk>/delete', views.BrandDelete.as_view(), name="brand-delete"),
    path('brand/<int:pk>/', views.BrandDetailView.as_view(), name="brand-detail"),
    path('brand', views.BrandListView.as_view(), name="brand-list"),
    # Autocomplete
    path('autocomplete/company', views.CompanyAutocomplete.as_view(), name='company-autocomplete'),
    path(r'autocomplete/brand/', views.BrandAutocomplete.as_view(), name='brand-autocomplete'),
]
