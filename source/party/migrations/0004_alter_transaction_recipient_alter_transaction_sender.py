# Generated by Django 4.1.13 on 2024-03-09 23:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('party', '0003_alter_transaction_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='recipient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='recipient_transactions', to=settings.AUTH_USER_MODEL, verbose_name='Получатель'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sender_transactions', to=settings.AUTH_USER_MODEL, verbose_name='Отправитель'),
        ),
    ]
