from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("home",homepage,name='home'),
    path('',loginpage,name='login'),
    path('logout',logoutpage,name='logout'),
    path('register',registerpage,name='register'),
    path('profile',profilepage,name='profile'),
    path('profileedit',profileedit,name='proedit'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)