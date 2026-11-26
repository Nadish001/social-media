from django.contrib.auth.models import User
from .models import *
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver



@receiver(post_save,sender=User)
def addprofile(sender, instance, created, **kwargs):
    if created:         
        user = instance    
        Profile.objects.create(
            user=user
        )
