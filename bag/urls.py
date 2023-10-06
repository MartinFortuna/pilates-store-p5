from django.urls import path
from bag import views as bagViews

urlpatterns = [
    path('', bagViews.view_bag, name='bag'),
    path('add/<item_id>/', bagViews.add_to_bag, name='add_to_bag'),
]
