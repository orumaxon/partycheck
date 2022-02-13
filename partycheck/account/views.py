from django.contrib.auth import authenticate, login, views
from django.shortcuts import redirect
from django.views import generic

from account.forms import SignInForm, SignUpForm
from account.models import User


class SignInView(views.LoginView):
    form_class = SignInForm
    redirect_authenticated_user = True
    template_name = 'account/signin.html'

    def get_success_url(self):
        return '/'


class SignUpView(generic.FormView):
    form_class = SignUpForm
    template_name = 'account/signup.html'

    def get_success_url(self):
        return '/'

    def form_valid(self, form):
        form.save()
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


class SingOutView(views.LogoutView):
    next_page = '/'


class AccountDetailView(generic.DetailView):
    model = User
    template_name = 'account/account.html'
