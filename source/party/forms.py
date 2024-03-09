from django import forms

from common.forms.mixins import DefaultAttrWidgetMixin
from party.models import Party, Payment


class PartyCreateForm(DefaultAttrWidgetMixin, forms.ModelForm):
    attrs_widget_model = Party

    class Meta:
        model = Party
        fields = ['name', 'members']


class PartyUpdateForm(PartyCreateForm):
    pass


class PaymentCreateForm(DefaultAttrWidgetMixin, forms.ModelForm):
    attrs_widget_model = Party

    class Meta:
        model = Payment
        fields = ['price', 'debtors', 'comment']
