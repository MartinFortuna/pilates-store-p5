from django.urls import path
from bag import views as bagViews

urlpatterns = [
    path('', bagViews.view_bag, name='bag'),
    path('add/<item_id>/', bagViews.add_to_bag, name='add_to_bag'),
    path('remove_from_bag/<item_id>/',
         bagViews.remove_from_bag, name='remove_from_bag'),
    path('update_bag/<item_id>/', bagViews.update_bag, name='update_bag'),
]
