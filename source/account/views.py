from django.contrib.auth import authenticate, login, views
from django.views import generic

from .forms import SignInForm, SignUpForm
from .models import User


class SignInView(views.LoginView):
    form_class = SignInForm
    template_name = 'account/signin.html'
    redirect_authenticated_user = True
    next_page = '/'


class SignUpView(generic.FormView):
    form_class = SignUpForm
    template_name = 'account/signup.html'
    next_page = '/'

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
