from django.urls import path
from django.views.generic import TemplateView

app_name = 'account'
urlpatterns = [
    path('signin/', TemplateView.as_view(template_name='account/signin.html'), name='signin'),
    path('signup/', TemplateView.as_view(template_name='account/signup.html'), name='signup'),
]
