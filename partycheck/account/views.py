from django.contrib.auth import views

from account.forms import SignInForms


class SignInView(views.LoginView):
    form_class = SignInForms
    redirect_authenticated_user = True

    def get_success_url(self):
        return '/'


class SingOutView(views.LogoutView):
    next_page = '/'

