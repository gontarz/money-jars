from django.contrib import admin

# Register your models here.

from money_jars.models import Currency, Jar, Operation, Transaction


class ReadOnlyFieldsMixIn:
    readonly_fields = (
        'created',
        'updated'
    )


class CurrencyAdmin(ReadOnlyFieldsMixIn, admin.ModelAdmin):
    pass


class JarAdmin(ReadOnlyFieldsMixIn, admin.ModelAdmin):
    pass


class OperationAdmin(ReadOnlyFieldsMixIn, admin.ModelAdmin):
    pass


class TransactionAdmin(ReadOnlyFieldsMixIn, admin.ModelAdmin):
    pass


admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Jar, JarAdmin)
admin.site.register(Operation, OperationAdmin)
admin.site.register(Transaction, TransactionAdmin)
