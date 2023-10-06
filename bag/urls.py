from django.urls import path
from bag import views as bagViews

urlpatterns = [
    path('', bagViews.view_bag, name='bag'),
]
