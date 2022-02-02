from django.contrib import admin
from .models import ProductImage, Product, OrderItem, Order, BasketItem, PrePaymentOrder


class ImageInLine(admin.StackedInline):
    model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageInLine]


admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(PrePaymentOrder)
admin.site.register(OrderItem)
admin.site.register(BasketItem)

# Register your models here.
