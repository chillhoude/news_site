from .views import *
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('login/',login_user,name='login'),
    path('logout/',logout_user,name='logout'),
    path('register/',register,name='register'),
    path('cabinet/',cabinet,name='cabinet'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)