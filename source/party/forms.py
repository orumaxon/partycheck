from django import forms

from common.forms.mixins import DefaultAttrWidgetMixin
from .models import Debt, Party, Payment, Transaction
from account.models import User


class PartyCreateForm(DefaultAttrWidgetMixin, forms.ModelForm):
    class Meta:
        model = Party
        fields = ['name', 'members']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        users = User.objects.exclude(is_superuser=True)
        self.fields['members'].queryset = users


class PartyUpdateForm(PartyCreateForm):
    pass


class PaymentCreateForm(DefaultAttrWidgetMixin, forms.ModelForm):
    on_all = forms.BooleanField(label='Поделить на всех поровну', required=False)

    class Meta:
        model = Payment
        fields = ['price', 'comment']


class DebtCreateForm(DefaultAttrWidgetMixin, forms.ModelForm):
    class Meta:
        model = Debt
        fields = ['debtor', 'price', 'comment']

    def __init__(self, party_id=None, **kwargs):
        super().__init__(**kwargs)
        users = User.objects.filter(members_parties__id=party_id)
        self.fields['debtor'].queryset = users
        self.fields['debtor'].empty_label = 'Выберите из списка'


class TransactionCreateForm(DefaultAttrWidgetMixin, forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['recipient', 'value', 'comment']

    def __init__(self, user=None, party_id=None, **kwargs):
        super().__init__(**kwargs)
        users = User.objects.filter(members_parties__id=party_id).exclude(id=user.id)
        self.fields['recipient'].queryset = users
        self.fields['recipient'].empty_label = 'Выберите из списка'
