from django.contrib import admin
from .models import *

# Register your models here.
class Product_OrderInline(admin.TabularInline):
    model = Product_Order
    extra = 0

class StatusAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Status._meta.fields]

    class Meta:
        model = Status

admin.site.register(Status, StatusAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]
    inlines = [Product_OrderInline]

    class Meta:
        model = Order

admin.site.register(Order, OrderAdmin)

class Product_OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product_Order._meta.fields]

    class Meta:
        model = Order

admin.site.register(Product_Order, Product_OrderAdmin)

class ProductInBasketAdmin (admin.ModelAdmin):
    list_display = [field.name for field in ProductInBasket._meta.fields]

    class Meta:
        model = ProductInBasket

admin.site.register(ProductInBasket, ProductInBasketAdmin)