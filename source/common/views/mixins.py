from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.urls import reverse


class SigninRequiredMixin(LoginRequiredMixin):
    def get_login_url(self):
        return reverse('account:signin')


class CacheManager:

    @staticmethod
    def clear(cache_name: str, cache_args: list = None):
        key = make_template_fragment_key(cache_name, cache_args)
        return cache.delete(key)

    @staticmethod
    def get(cache_name: str, cache_args: list = None):
        key = make_template_fragment_key(cache_name, cache_args)
        return cache.get(key)

    @staticmethod
    def set(cache_name: str, value, cache_args: list = None, **kwargs):
        key = make_template_fragment_key(cache_name, cache_args)
        return cache.set(key, value, **kwargs)

    @staticmethod
    def get_or_set(cache_name: str, default, cache_args: list = None, **kwargs):
        key = make_template_fragment_key(cache_name, cache_args)
        return cache.get_or_set(key, default, **kwargs)


class CacheMixin:
    _cache_manager = CacheManager

    @property
    def cache(self):
        return self._cache_manager()
