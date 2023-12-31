from django.urls import path
from products import views as productViews

urlpatterns = [
    path('', productViews.all_products, name='products'),
    path(
        '<int:product_id>/',
        productViews.product_detail,
        name='product_detail'
    ),
    path(
        'rate_product/<int:product_id>/',
        productViews.rate_product,
        name='rate_product'
    ),
    path('add_product/', productViews.add_product, name='add_product'),
    path(
        'update_product/<int:product_id>/',
        productViews.update_product,
        name='update_product'
    ),
    path(
        'delete/<int:product_id>/',
        productViews.delete_product,
        name='delete_product'
    ),
]
