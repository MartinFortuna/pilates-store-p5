from django.contrib import admin

from .models import CategoryProduct, Product, SizeProduct, RateProduct, InventoryProduct

# Register your models here.

admin.site.register(Product)
admin.site.register(InventoryProduct)
admin.site.register(RateProduct)
admin.site.register(CategoryProduct)
admin.site.register(SizeProduct)