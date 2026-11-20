from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.utils.http import url_has_allowed_host_and_scheme


# Create your views here.
def homepage(request):
    return render(request,'home.html')

def registerpage(request):
    if request.method == 'POST':
        form =Registerform(request.POST)
        if form.is_valid():
            usr=form.save()
            # usr = form.save()
            # Profile.objects.create(user=usr)
            # form.save()
            messages.success(request,"user registered successfully ")
            # send_mail("welcome mail",f"welcome to our app {usr.username} thanking you for trusting us",settings.EMAIL_HOST_USER,[usr.email])
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


def logoutpage(request):
    logout(request)
    messages.success(request,"user loggedout successfully ")
    return redirect(loginpage)


def profilepage(request):
    pro = Profile.objects.get(user = request.user)
    context = {
        'pro': pro,
        'posts': Posts.objects.filter(user=request.user).order_by('-id'),
        'tagged': Posts.objects.filter(tagged=request.user).order_by('-id'),
        'saved': Posts.objects.filter(saved_by=request.user).order_by('-id'),
    }
    return render(request, 'profile.html', context)
    

def profileedit(request):
    pro = Profile.objects.get(user=request.user)
    if request.method =='POST':
        form = Profileform(request.POST,request.FILES,instance=pro)
        if form.is_valid():
            form.save()
            return redirect(profilepage)
    else:
        form = Profileform(instance=pro)
    return render(request,'profileedit.html',{"form":form})


def postpage(request):
    if request.method == 'POST':
        form = Postform(request.POST, request.FILES)
        form.fields['tagged'].queryset = User.objects.exclude(id=request.user.id)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.save()
            form.save_m2m()          # saves the tagged people
            return redirect(profilepage)
    else:
        form = Postform()
        form.fields['tagged'].queryset = User.objects.exclude(id=request.user.id)
    return render(request, 'postpage.html', {'form': form})


def postedit(request, pid):
    pro = Posts.objects.get(id=pid, user=request.user)
    if request.method == 'POST':
        form = Postform(request.POST, request.FILES, instance=pro)
        form.fields['tagged'].queryset = User.objects.exclude(id=request.user.id)
        if form.is_valid():
            form.save()
            return redirect(profilepage)
    else:
        form = Postform(instance=pro)
        form.fields['tagged'].queryset = User.objects.exclude(id=request.user.id)
    return render(request, 'postedit.html', {"form": form, "post": pro})


def postdelete(request, pid):
    pro = Posts.objects.get(id=pid, user=request.user)
    pro.delete()
    return redirect(profilepage)


def postview(request, pid):
    post = Posts.objects.get(id=pid)
    is_saved = post.saved_by.filter(id=request.user.id).exists()
    return render(request, 'postview.html', {'post': post, 'is_saved': is_saved})


def postsave(request, pid):
    post = Posts.objects.get(id=pid)
    if post.saved_by.filter(id=request.user.id).exists():
        post.saved_by.remove(request.user)
    else:
        post.saved_by.add(request.user)
    nxt = request.POST.get('next')
    if nxt and url_has_allowed_host_and_scheme(nxt, allowed_hosts={request.get_host()}):
        return redirect(nxt)
    return redirect('postview', pid=pid)





def explore(request):
    q = request.GET.get('q', '').strip()
    posts = Posts.objects.select_related('user').order_by('-id')
    if q:
        posts = posts.filter(
            Q(title__icontains=q) | Q(des__icontains=q) | Q(user__username__icontains=q)
        )
    saved_ids = set(Posts.objects.filter(saved_by=request.user).values_list('id', flat=True))
    return render(request, 'explore.html', {'posts': posts, 'saved_ids': saved_ids, 'q': q})