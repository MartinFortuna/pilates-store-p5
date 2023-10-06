from django.urls import path
from products import views as productViews

urlpatterns = [
    path('', productViews.all_products, name='products'),
    path('<int:product_id>/', productViews.product_detail, name='product_detail'),
]