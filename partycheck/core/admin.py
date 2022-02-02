from django.contrib import admin

from .models import *


@admin.register(PartyGroup)
class PartyGroupAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'created_at']
    readonly_fields = ['created_at']
    raw_id_fields = ['creator']
    filter_horizontal = ['members']


@admin.register(PartyPayment)
class PartyPaymentAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'created_at']
    readonly_fields = ['created_at']
    raw_id_fields = ['party_group', 'investor']
    filter_horizontal = ['debtors']


@admin.register(PartyTransaction)
class PartyTransactionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'created_at']
    readonly_fields = ['created_at']
    raw_id_fields = ['party_group', 'sender', 'recipient']

