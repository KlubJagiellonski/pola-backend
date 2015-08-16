from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Count

from . import models

# class CompanyListView(ListView, SortMixin, FilterMixin):
#     model = models.Product
#     default_sort_params = ('popularity', 'name')
#     default_filter_param = 'all'

#     def get_queryset(self, **kwargs):
#         query = super(CompanyListView, self).get_queryset(**kwargs)
#         return query

#     def sort_queryset(self, qs, sort_by, order):
#         if sort_by == 'popularity':
#             qs = qs.annotate(
#                 query_count=Count('Query')).order_by('query_count')
#         if order == 'name':
#             qs = qs.reverse()
#         return qs

#     def filter_queryset(self, qs, filter_param):
#         if filter_param == 'empty':
#             qs = qs.filter(productIn__isnull=True)
#         return qs
