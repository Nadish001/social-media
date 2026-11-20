from django.contrib.auth.models import User
from .models import *
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver

# if user created then need to create an profile using this user 

@receiver(post_save,sender=User)
def addprofile(sender, instance, created, **kwargs):
    if created:         #check if the object has been created
        user = instance     #instance of sender means obj of cls
        Profile.objects.create(
            user=user
        )

@receiver(post_delete,sender=User)
def delprofile(sender,instance,**kwargs):
    Profile.objects.delete(user=sender)