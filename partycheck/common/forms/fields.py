from django import forms

from .widgets import CurrentPasswordInput, NewPasswordInput


class CurrentPasswordField(forms.CharField):
    widget = CurrentPasswordInput()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, strip=False, **kwargs)


class NewPasswordField(forms.CharField):
    widget = NewPasswordInput()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, strip=False, **kwargs)
