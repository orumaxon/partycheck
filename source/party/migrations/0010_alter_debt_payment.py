# Generated by Django 4.1.13 on 2024-03-10 21:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('party', '0009_rename_debtors_debt_alter_debt_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='debt',
            name='payment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='debts', to='party.payment', verbose_name='Расход'),
        ),
    ]
