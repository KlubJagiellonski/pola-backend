from django.conf import settings
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.http import JsonResponse
from django.utils.functional import cached_property
from django.views import View
from django.views.generic import DetailView, ListView
from google.api_core import exceptions as gcs_exceptions

from pola.ai_pics.models import AIAttachment, AIPics
from pola.gcs import get_bucket


class BucketMixin:
    @property
    def _bucket(self):
        return get_bucket(settings.GCS_AI_PICS_BUCKET_NAME)


class AIPicsPageView(LoginRequiredMixin, PermissionRequiredMixin, BucketMixin, ListView):
    permission_required = 'ai_pics.view_aipics'
    ordering = '-id'
    paginate_by = 10
    model = AIPics

    def get_queryset(self):
        qs = super().get_queryset()
        if self.state == 'valid':
            qs = qs.filter(is_valid=True)
        elif self.state == 'invalid':
            qs = qs.filter(is_valid=False)
        else:
            qs = qs.filter(is_valid__isnull=True)

        return qs.prefetch_related('aiattachment_set')

    @cached_property
    def state(self):
        return self.request.GET.get('state', 'unknown')

    def get_context_data(self, *args, **kwargs):
        kwargs['state'] = self.state
        return super().get_context_data(**kwargs)

    def post(self, request):
        action_name = self.request.POST['action']
        fn = getattr(self, f'action_{action_name}', None)
        if fn:
            return fn(request)

        return self.get(request)


class ApiSetAiPicStateView(View, PermissionRequiredMixin, BucketMixin):
    permission_required = 'ai_pics.change_aipics'

    def post(self, request):
        id = request.POST['id']
        state = request.POST['state']
        aipic = AIPics.objects.get(id=id)
        aipic.state = state
        aipic.save()
        return JsonResponse({'ok': True})


class ApiDeleteAiPicsView(View, PermissionRequiredMixin, BucketMixin):
    permission_required = 'ai_pics.delete_aipics'

    def post(self, request):
        id = request.POST['id']

        attachments = AIAttachment.objects.filter(ai_pics_id=id)
        for attachment in attachments:
            blob = self._bucket.blob(attachment.attachment.name)
            try:
                blob.delete()
            except gcs_exceptions.NotFound:
                pass

        aipic = AIPics.objects.get(id=id)
        aipic.delete()
        return JsonResponse({'ok': True})


class ApiDeleteAttachmentView(View, PermissionRequiredMixin, BucketMixin):
    permission_required = 'ai_pics.delete_aiattachment'

    def post(self, request):
        id = request.POST['id']
        attachment = AIAttachment.objects.get(id=id)

        blob = self._bucket.blob(attachment.attachment.name)
        try:
            blob.delete()
        except gcs_exceptions.NotFound:
            pass

        attachment.delete()
        return JsonResponse({'ok': True})


class AIPicsDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'ai_pics.view_aipics'
    model = AIPics

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.prefetch_related('aiattachment_set')
