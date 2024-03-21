from django.urls import path

from .views import AccountView, SignInView, SignUpView, SingOutView

app_name = 'account'
urlpatterns = [
    path('signin/', SignInView.as_view(), name='signin'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signout/', SingOutView.as_view(), name='signout'),
    path('', AccountView.as_view(), name='account'),
]
