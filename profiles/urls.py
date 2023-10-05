from django.urls import path
from profiles import views as profileViews

urlpatterns = [
    path('', profileViews.user_profile, name='user_profile'),
    path('update_profile/', profileViews.update_profile, name='update_profile'),
]
