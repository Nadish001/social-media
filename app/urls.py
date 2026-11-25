from django.urls import path
from .views import *

urlpatterns = [
    path("home",homepage,name='home'),
    path('follow-suggestions', follow_suggestions, name='follow_suggestions'),
    path('',loginpage,name='login'),
    path('logout',logoutpage,name='logout'),
    path('register',registerpage,name='register'),
    path('profile',profilepage,name='profile'),
    path('profile/<str:username>',userprofile,name='userprofile'),
    path('follow/<str:username>',follow_user,name='follow_user'),
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