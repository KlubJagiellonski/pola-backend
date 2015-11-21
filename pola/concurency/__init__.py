from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured
from django.utils.encoding import force_text
from django.views.generic.edit import BaseUpdateView
from django.http import HttpResponseRedirect


class BaseConcurency(object):
    def is_locked(obj, user):
        raise NotImplementedError(
            'subclasses of BaseConcurency must \
            provide a is_locked(obj, user) method')

    def lock(obj, user):
        raise NotImplementedError(
            'subclasses of BaseConcurency must \
            provide a lock(obj, user) method')

    def unlock(obj):
        raise NotImplementedError(
            'subclasses of BaseConcurency must \
            provide a unlock(obj, user) method')


class CacheConcurency(BaseConcurency):
    def _make_key(self, obj):
        obj_name = obj.__class__.__name__
        pk = obj.pk
        return 'concurency_' + obj_name + '_' + str(pk)

    def is_locked(self, obj, user):
        key = self._make_key(obj)
        lock_pk = cache.get(key)
        if not lock_pk:
            return False
        return user.pk != lock_pk

    def lock(self, obj, user):
        key = self._make_key(obj)
        return cache.set(key, user.pk)

    def unlock(self, obj):
        key = self._make_key(obj)
        cache.delete(key)

concurency = CacheConcurency()


class ConcurencyProtectUpdateView(object):
    def get_concurency(self):
        return concurency

    def get_concurency_url(self):
        if self.concurency_url:
            return force_text(self.concurency_url)
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a concurency_url.")

    def dispatch(self, request, *args, **kwargs):
        concurency = self.get_concurency()
        obj = self.get_object()
        concurency_url = self.get_concurency_url()
        if concurency.is_locked(obj, request.user):
            return HttpResponseRedirect(concurency_url)
        concurency.lock(obj, request.user)
        return super(
            ConcurencyProtectUpdateView,
            self).dispatch(request, *args, **kwargs)

    def form_valid(self, *args, **kwargs):
        concurency = self.get_concurency()
        obj = self.get_object()
        concurency.unlock(obj)
        return super(
            ConcurencyProtectUpdateView,
            self).form_valid(*args, **kwargs)
