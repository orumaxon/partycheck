from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms
from django.utils.translation import gettext_lazy as _


class SignInForms(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={
            'class': 'form-control my-2',
        })
    )
    password = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'class': 'form-control my-2',
        }),
    )
