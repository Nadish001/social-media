from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    # phone = models.IntegerField(null=True)
    pro_pic  = models.ImageField(upload_to='profile',blank=True)
    def __str__(self):
        return self.user.username

class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    des = models.TextField(blank=True)
    post_img = models.ImageField(upload_to='posts')
    tagged = models.ManyToManyField(User, related_name='tagged_posts', blank=True)
    saved_by = models.ManyToManyField(User, related_name='saved_posts', blank=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)   # new


class Comment(models.Model):                                                       # new
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)