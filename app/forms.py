from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.forms import ValidationError

class Registerform(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email']

class Profileform(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        widgets = {
        'bio': forms.TextInput(attrs={
        'class' :'form-control',
        'placeholde':'enter your  bio'
        }),
     }

class Postform(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ('post_img', 'title', 'des', 'tagged')
        widgets = {'tagged': forms.SelectMultiple(attrs={'size': 5})}