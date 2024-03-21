from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.urls import reverse


class SigninRequiredMixin(LoginRequiredMixin):
    def get_login_url(self):
        return reverse('account:signin')


class CacheViewMixin:

    @staticmethod
    def clear_cache(cache_name: str = None, cache_args: list = None):
        key = make_template_fragment_key(cache_name, cache_args)
        cache.delete(key)
