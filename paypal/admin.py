from django.contrib import admin
from paypal.models import PayPalOrder, PayPalPurchaseUnit, PayPalItem, PayPalMerchant, PayPalShippingAddress, PayPalPayer


class PayPalPurchaseUnitInLine(admin.StackedInline):
    model = PayPalPurchaseUnit


class PayPalOrderAdmin(admin.ModelAdmin):
    inlines = [PayPalPurchaseUnitInLine]


admin.site.register(PayPalOrder, PayPalOrderAdmin)
admin.site.register(PayPalPayer)
admin.site.register(PayPalPurchaseUnit)
admin.site.register(PayPalItem)
admin.site.register(PayPalMerchant)
admin.site.register(PayPalShippingAddress)