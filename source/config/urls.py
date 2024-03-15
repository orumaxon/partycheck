from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'home.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('account:profile')
        return super().dispatch(request, *args, **kwargs)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('party/', include('party.urls')),
    path('', HomeView.as_view()),

    path('__debug__/', include('debug_toolbar.urls')),
]
