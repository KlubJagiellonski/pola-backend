from boto.s3.connection import S3Connection, Bucket, Key
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.functional import cached_property
from django.views.generic import ListView

from ai_pics.models import AIPics, AIAttachment


class AIPicsPageView(LoginRequiredMixin, ListView):
    ordering = '-id'
    paginate_by = 10
    model = AIPics

    def get_queryset(self):
        qs = super(AIPicsPageView, self).get_queryset()
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
        return super(AIPicsPageView, self).get_context_data(**kwargs)

    def post(self, request):
        action_name = self.request.POST['action']
        fn = getattr(self, 'action_%s' % action_name, None)
        if fn:
            return fn(request)

        return self.get(request)

    def action_set_aipic_state(self, request):
        id = request.POST['id']
        state = request.POST['state']
        aipic = AIPics.objects.get(id=id)
        aipic.state = state
        aipic.save()
        return JsonResponse({'ok': True})

    def action_delete_attachment(self, request):
        key = Key(self._bucket)

        id = request.POST['id']
        attachment = AIAttachment.objects.get(id=id)

        key.key = attachment.attachment
        self._bucket.delete_key(key)

        attachment.delete()
        return JsonResponse({'ok': True})

    def action_delete_aipic(self, request):
        key = Key(self._bucket)

        id = request.POST['id']

        attachments = AIAttachment.objects.filter(ai_pics_id=id)
        for attachment in attachments:
            key.key = attachment.attachment
            self._bucket.delete_key(key)

        aipic = AIPics.objects.get(id=id)
        aipic.delete()
        return JsonResponse({'ok': True})

    @property
    def _bucket(self):
        conn = S3Connection(settings.AWS_ACCESS_KEY_ID,
                            settings.AWS_SECRET_ACCESS_KEY)
        bucket = Bucket(conn, settings.AWS_STORAGE_BUCKET_AI_NAME)
        return bucket
