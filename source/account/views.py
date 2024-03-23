from django.contrib.auth import authenticate, login, views
from django.views import generic

from common.views.mixins import CacheMixin, SigninRequiredMixin

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
    success_url = '/'

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


class AccountView(SigninRequiredMixin, CacheMixin, generic.TemplateView):
    model = User
    template_name = 'account/account.html'

    def get_debts_and_payments_info(self):
        user = self.request.user
        cache_args = [user.id, user.username]

        full_debts = self.cache.get_or_set('user_full_debts', user.get_full_debts, cache_args, timeout=10)
        full_payments = self.cache.get_or_set('user_full_payments', user.get_full_payments, cache_args, timeout=10)

        return full_debts, full_payments

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        full_debts, full_payments = self.get_debts_and_payments_info()
        context['full_debts'] = full_debts
        context['full_payments'] = full_payments
        return context
