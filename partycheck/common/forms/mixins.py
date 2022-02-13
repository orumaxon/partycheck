from django.core.exceptions import FieldDoesNotExist


class DefaultAttrWidgetMixin:
    attrs_widget_model = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_widget_attrs(self.fields)

    def set_default_widget_attrs(self, form_fields):
        for field_name in form_fields:
            form_fields[field_name].widget.attrs['class'] = 'form-control my-2'
            try:
                model_field = self.attrs_widget_model._meta.get_field(field_name)
                form_fields[field_name].widget.attrs['placeholder'] = model_field.verbose_name.capitalize()
            except FieldDoesNotExist:
                form_fields[field_name].widget.attrs['placeholder'] = form_fields[field_name].label
