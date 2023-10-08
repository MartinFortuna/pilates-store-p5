from django.urls import path
from checkout import views as checkoutViews
from .webhooks import webhook

urlpatterns = [
    path('', checkoutViews.checkout, name='checkout'),
    path('checkout_success/<order_number>',
         checkoutViews.checkout_success,
         name='checkout_success'),
    path('cache_checkout_data/',
         checkoutViews.cache_checkout_data,
         name='cache_checkout_data'),
    path('wh/', webhook, name='webhook'),
]
