from django.urls import path
from checkout import views as checkoutViews

urlpatterns = [
    path('', checkoutViews.checkout, name='checkout'),
    path('checkout_success', checkoutViews.checkout, name='checkout_success'),
]