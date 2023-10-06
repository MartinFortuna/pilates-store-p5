from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from home import views as homeViews

urlpatterns = [
    path('', homeViews.index, name='home'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
