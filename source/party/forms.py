from django import forms

from common.forms.mixins import DefaultAttrWidgetMixin
from party.models import Party, Payment, Transaction


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
