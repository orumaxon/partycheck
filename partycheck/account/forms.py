from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.core.exceptions import ValidationError

from common.forms.mixin import DefaultAttrWidgetMixin

UserModel = get_user_model()


class SignInForms(AuthenticationForm, DefaultAttrWidgetMixin):
    username = UsernameField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}), strip=False)

    error_messages = {
        'invalid_login': 'Упс... Не верный ник или пароль.',
        'inactive': 'Данный аккаунт не активный',
    }

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.set_default_widget_attrs(self.fields, UserModel)

    def get_invalid_login_error(self):
        self.fields['username'].widget.attrs['class'] += ' is-invalid'
        self.fields['password'].widget.attrs['class'] += ' is-invalid'
        return ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
        )
