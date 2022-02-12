
class DefaultAttrWidgetMixin:

    @staticmethod
    def set_default_widget_attrs(fields, model):
        for field_name in fields:
            model_field = model._meta.get_field(field_name)
            fields[field_name].widget.attrs['placeholder'] = model_field.verbose_name.capitalize()
            fields[field_name].widget.attrs['class'] = 'form-control my-2'
