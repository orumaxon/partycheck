from django.urls import path
from django.views.generic import TemplateView

from .views import SignInView, SingOutView

app_name = 'account'
urlpatterns = [
    path('signin/', SignInView.as_view(template_name='account/signin.html'), name='signin'),
    path('signout/', SingOutView.as_view(), name='signout'),

    path('signup/', TemplateView.as_view(template_name='account/signup.html'), name='signup'),
]
