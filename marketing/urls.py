from django.urls import path
from marketing import views as marketingViews

urlpatterns = [
    path('newsletter', marketingViews.subscribe_newsLetter, name='newsLetter'),
    path(
        'unsubscribe',
        marketingViews.unsubscribe_newsletter,
        name='unsubscribe'
    ),
]
