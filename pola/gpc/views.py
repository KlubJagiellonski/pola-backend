from braces.views import FormValidMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, UpdateView
from django_filters.views import FilterView

from ..mixins import LoginPermissionRequiredMixin
from . import filters, forms, models


class GPCBrickDetailView(LoginRequiredMixin, DetailView):
    slug_field = 'code'
    model = models.GPCBrick


class GPCBrickListView(LoginRequiredMixin, FilterView):
    model = models.GPCBrick
    filterset_class = filters.GPCBrickFilter
    paginate_by = 25


class GPCBrickUpdateView(LoginPermissionRequiredMixin, FormValidMessageMixin, UpdateView):
    permission_required = 'gpc.change_gpcbrick'
    slug_field = 'code'
    model = models.GPCBrick
    form_class = forms.GPCBrickForm
    form_valid_message = _("Brick zaktualizowany!")


class GPCClassDetailView(LoginRequiredMixin, DetailView):
    slug_field = 'code'
    model = models.GPCClass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = context['object']

        context['brick_list'] = models.GPCBrick.objects.filter(parent=obj)

        return context


class GPCClassListView(LoginRequiredMixin, FilterView):
    model = models.GPCClass
    filterset_class = filters.GPCClassFilter
    paginate_by = 25


class GPCClassUpdateView(LoginPermissionRequiredMixin, FormValidMessageMixin, UpdateView):
    permission_required = 'gpc.change_gpcclass'
    slug_field = 'code'
    model = models.GPCClass
    form_class = forms.GPCClassForm
    form_valid_message = _("Klasa zaktualizowany!")


class GPCFamilyDetailView(LoginRequiredMixin, DetailView):
    slug_field = 'code'
    model = models.GPCFamily

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = context['object']

        context['class_list'] = models.GPCClass.objects.filter(parent=obj)

        return context


class GPCFamilyListView(LoginRequiredMixin, FilterView):
    model = models.GPCFamily
    filterset_class = filters.GPCFamilyFilter
    paginate_by = 25


class GPCFamilyUpdateView(LoginPermissionRequiredMixin, FormValidMessageMixin, UpdateView):
    permission_required = 'gpc.change_gpcfamily'
    slug_field = 'code'
    model = models.GPCFamily
    form_class = forms.GPCFamilyForm
    form_valid_message = _("Rodzina zaktualizowany!")


class GPCSegmentDetailView(LoginRequiredMixin, DetailView):
    slug_field = 'code'
    model = models.GPCSegment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = context['object']

        context['family_list'] = models.GPCFamily.objects.filter(parent=obj)

        return context


class GPCSegmentListView(LoginRequiredMixin, FilterView):
    model = models.GPCSegment
    filterset_class = filters.GPCSegmentFilter
    paginate_by = 25


class GPCSegmentUpdateView(LoginPermissionRequiredMixin, FormValidMessageMixin, UpdateView):
    permission_required = 'gpc.change_gpcsegment'
    slug_field = 'code'
    model = models.GPCSegment
    form_class = forms.GPCSegmentForm
    form_valid_message = _("Segment zaktualizowany!")
