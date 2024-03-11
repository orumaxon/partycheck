from django.core.exceptions import FieldDoesNotExist
from django import forms


class DefaultAttrWidgetMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_widget_attrs(self.fields)

    def set_default_widget_attrs(self, form_fields):
        for field_name in form_fields:
            form_field = form_fields[field_name]

            if form_field.required:
                form_field.label_suffix = '*:'

            if isinstance(form_field, forms.BooleanField):
                form_field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(form_field, forms.ModelChoiceField):
                form_field.widget.attrs['class'] = 'form-select'
            else:
                form_field.widget.attrs['class'] = 'form-control my-2'

            try:
                model_field = self.Meta.model._meta.get_field(field_name)
                form_field.widget.attrs['placeholder'] = model_field.verbose_name.capitalize()
            except FieldDoesNotExist:
                form_field.widget.attrs['placeholder'] = form_fields[field_name].label

    def clean(self):
        for error_field in self.errors:
            self.fields[error_field].widget.attrs['class'] += ' is-invalid'
        return super().clean()
