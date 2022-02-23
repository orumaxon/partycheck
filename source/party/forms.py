from django import forms

from common.forms.mixins import DefaultAttrWidgetMixin
from party.models import Party


class PartyCreateForm(DefaultAttrWidgetMixin, forms.ModelForm):
    attrs_widget_model = Party

    class Meta:
        model = Party
        fields = ['name', 'members']
