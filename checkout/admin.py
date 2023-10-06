from django.contrib import admin
from .models import Order, OrderItem
from profiles.models import UserDetail

# Register your models here.

class OrderItem(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('subtotal', 'size')


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItem,)

    readonly_fields = ('order_number', 'shipping_details_html', 'date', 'total_items', 'delivery_cost', 'grand_total', 'original_bag', 'stripe_pid')

    list_display = ('user', 'order_number', 'date', 'total_items', 'delivery_cost', 'grand_total')

admin.site.register(Order, OrderAdmin)