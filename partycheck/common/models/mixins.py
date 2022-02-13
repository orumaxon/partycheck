from django.db import models


class CreatedAtMixin(models.Model):
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    class Meta:
        abstract = True
