from django.contrib import admin

from .models import *


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'created_at']
    readonly_fields = ['created_at']
    raw_id_fields = ['creator']
    filter_horizontal = ['members']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'party', 'created_at']
    readonly_fields = ['created_at']
    raw_id_fields = ['party', 'investor']
    filter_horizontal = ['debtors']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'created_at']
    readonly_fields = ['created_at']
    raw_id_fields = ['party', 'sender', 'recipient']

