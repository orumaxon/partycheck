from django.forms import PasswordInput


class CurrentPasswordInput(PasswordInput):
    def __init__(self, attrs=None):
        attrs = attrs or {}
        super().__init__({
            'autocomplete': 'current-password',
            **attrs,
        })


class NewPasswordInput(PasswordInput):
    def __init__(self, attrs=None):
        attrs = attrs or {}
        super().__init__({
            'autocomplete': 'new-password',
            **attrs,
        })
