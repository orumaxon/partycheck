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
    raw_id_fields = ['party', 'sponsor']
    filter_horizontal = ['py_debtors']


@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    raw_id_fields = ['payment', 'debtor']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'created_at']
    readonly_fields = ['created_at']
    raw_id_fields = ['party', 'sender', 'recipient']
