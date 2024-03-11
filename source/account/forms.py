from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.core.exceptions import ValidationError

from common.forms.fields import CurrentPasswordField, NewPasswordField
from common.forms.mixins import DefaultAttrWidgetMixin

UserModel = get_user_model()


class SignInForm(DefaultAttrWidgetMixin, AuthenticationForm):
    username = UsernameField()
    password = CurrentPasswordField()

    error_messages = {
        'invalid_login': 'Упс... Не верное имя пользователя или пароль.',
        'inactive': 'Данный аккаунт не активный',
    }

    class Meta:
        model = UserModel

    def get_invalid_login_error(self):
        self.fields['username'].widget.attrs['class'] += ' is-invalid'
        self.fields['password'].widget.attrs['class'] += ' is-invalid'
        return ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
        )


class SignUpForm(DefaultAttrWidgetMixin, forms.Form):
    username = UsernameField()
    password = NewPasswordField()
    password_repeat = NewPasswordField(label='Повторите пароль')

    attrs_widget_model = UserModel
    error_messages = {
        'password_mismatch': 'Упс... Введенные пароли не совпадают',
        'username_already_exists': 'Упс... Данное имя уже занято ¯\\_(ツ)_/¯',
    }

    class Meta:
        model = UserModel

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and UserModel.objects.filter(username=username).exists():
            raise forms.ValidationError(
                self.error_messages['username_already_exists'],
                code='username_already_exists',
            )
        return username

    def clean_password_repeat(self):
        password = self.cleaned_data.get('password')
        password_repeat = self.cleaned_data.get('password_repeat')
        if password and password_repeat and password != password_repeat:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password_repeat

    def save(self):
        user = UserModel.objects.create_user(
            username=self.cleaned_data.get('username'),
            password=self.cleaned_data.get('password'),
        )
        return user
