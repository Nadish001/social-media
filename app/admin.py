from django.contrib import admin
from .models import Follow, Posts, Profile

# Register your models here.
admin.site.register(Profile)
admin.site.register(Posts)
admin.site.register(Follow)
