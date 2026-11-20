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
    path('postpage',postpage,name='postpage'),
    path('postedit/<int:pid>',postedit,name='postedit'),
    path('postdelete/<int:pid>',postdelete,name='postdelete'),
    path('postview/<int:pid>', postview, name='postview'),
    path('postsave/<int:pid>', postsave, name='postsave'),
    path('explore', explore, name='explore'),
    path('postlike/<int:pid>', postlike, name='postlike'),
    path('commentadd/<int:pid>', commentadd, name='commentadd'),
    path('commentdelete/<int:cid>', commentdelete, name='commentdelete'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)