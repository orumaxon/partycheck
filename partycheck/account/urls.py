from django.urls import path
from django.views.generic import TemplateView

from .views import SignInView, SingOutView, AccountDetailView

app_name = 'account'
urlpatterns = [
    path('signin/', SignInView.as_view(template_name='account/signin.html'), name='signin'),
    path('signout/', SingOutView.as_view(), name='signout'),

    path('<int:pk>/', AccountDetailView.as_view(), name='detail'),

    path('signup/', TemplateView.as_view(template_name='account/signup.html'), name='signup'),
]
