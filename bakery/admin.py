from django.contrib import admin
from .models import Product, Order, OrderItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type', 'price', 'stock')
    list_filter = ('product_type',)
    search_fields = ('name',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order_date', 'order_type', 'status')
    list_filter = ('status', 'order_type', 'order_date')
    search_fields = ('customer__username', 'customer__email')
    inlines = (OrderItemInline,)
