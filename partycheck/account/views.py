from django.contrib.auth import views
from django.views import generic
from account.forms import SignInForms
from account.models import User


class SignInView(views.LoginView):
    form_class = SignInForms
    redirect_authenticated_user = True

    def get_success_url(self):
        return '/'


class SingOutView(views.LogoutView):
    next_page = '/'


class AccountDetailView(generic.DetailView):
    model = User
    template_name = 'account/account.html'
