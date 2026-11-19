from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
def homepage(request):
    return render(request,'home.html')

def registerpage(request):
    if request.method == 'POST':
        form =Registerform(request.POST)
        if form.is_valid():
            usr = form.save()
            Profile.objects.create(user=usr)
            # form.save()
            messages.success(request,"user registered successfully ")
            send_mail("welcome mail",f"welcome to our app {usr.username} thanking you for trusting us",settings.EMAIL_HOST_USER,[usr.email])
            return redirect(loginpage)
    else:
        form = Registerform()
    return render(request,'registerpage.html',{'form':form})

def loginpage(request):
    if request.method =='POST':
        n1=request.POST.get('n1')
        p1=request.POST.get('p1')
        # print(n1,p1)
        user = authenticate(request,username=n1,password=p1)
        if user:
            login(request,user)
            messages.success(request,"user loggedIn successfully ")
            return redirect(homepage)
        else:
            print("invalid creditential")
    return render(request,'loginpage.html')
