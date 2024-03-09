from django import forms

from common.forms.mixins import DefaultAttrWidgetMixin
from party.models import Party, Payment, Transaction
from account.models import User


class PartyCreateForm(DefaultAttrWidgetMixin, forms.ModelForm):
    attrs_widget_model = Party

    class Meta:
        model = Party
        fields = ['name', 'members']


class PartyUpdateForm(PartyCreateForm):
    pass


class PaymentCreateForm(DefaultAttrWidgetMixin, forms.ModelForm):
    attrs_widget_model = Payment

    class Meta:
        model = Payment
        fields = ['price', 'debtors', 'comment']


class TransactionCreateForm(DefaultAttrWidgetMixin, forms.ModelForm):
    attrs_widget_model = Transaction

    class Meta:
        model = Transaction
        fields = ['recipient', 'value', 'comment']

    def __init__(self, user=None, party_id=None, **kwargs):
        super().__init__(**kwargs)
        users = User.objects.filter(members__id=party_id).exclude(id=user.id)
        self.fields['recipient'].queryset = users
