from django.urls import path
from profiles import views as profileViews

urlpatterns = [
    path('', profileViews.user_profile, name='user_profile'),
    path('update_profile/', profileViews.update_profile, name='update_profile'),
    path('delete_profile/', profileViews.delete_profile, name='delete_profile'),
    path('order_history/<order_number>', profileViews.order_history, name='order_history'),
]
