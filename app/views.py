from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count, Q
from django.views.decorators.http import require_POST
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


@login_required
def profilepage(request):
    return _render_profile(request, request.user)


@login_required
def userprofile(request, username):
    profile_user = get_object_or_404(User, username=username)
    return _render_profile(request, profile_user)


def _render_profile(request, profile_user):
    pro = get_object_or_404(Profile, user=profile_user)
    is_own_profile = request.user == profile_user
    posts = Posts.objects.filter(user=profile_user).select_related('user').order_by('-id')
    tagged = Posts.objects.filter(tagged=profile_user).select_related('user').order_by('-id')
    saved = Posts.objects.filter(saved_by=profile_user).select_related('user').order_by('-id')
    context = {
        'pro': pro,
        'posts': posts,
        'tagged': tagged,
        'saved': saved if is_own_profile else Posts.objects.none(),
        'posts_count': posts.count(),
        'is_own_profile': is_own_profile,
        'is_following': not is_own_profile and Follow.objects.filter(
            follower=request.user, following=profile_user
        ).exists(),
        'followers_count': Follow.objects.filter(following=profile_user).count(),
        'following_count': Follow.objects.filter(follower=profile_user).count(),
    }
    return render(request, 'profile.html', context)
    

@login_required
@require_POST
def follow_user(request, username):
    profile_user = get_object_or_404(User, username=username)
    if profile_user == request.user:
        return redirect('profile')

    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=profile_user,
    )
    if not created:
        follow.delete()

    next_url = request.POST.get('next')
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect('userprofile', username=profile_user.username)


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


def go_back(request, pid):
    # return to the page the action came from, or to the post page
    nxt = request.POST.get('next')
    if nxt and url_has_allowed_host_and_scheme(nxt, allowed_hosts={request.get_host()}):
        return redirect(nxt)
    return redirect('postview', pid=pid)


def postview(request, pid):
    post = Posts.objects.select_related('user').prefetch_related('tagged').get(id=pid)
    can_follow = request.user.is_authenticated and post.user_id != request.user.id
    return render(request, 'postview.html', {
        'post': post,
        'is_saved': post.saved_by.filter(id=request.user.id).exists(),
        'is_liked': post.likes.filter(id=request.user.id).exists(),
        'is_following': can_follow and Follow.objects.filter(
            follower=request.user, following=post.user
        ).exists(),
        'can_follow': can_follow,
        'likes_count': post.likes.count(),
        'comments': post.comments.select_related('user').order_by('created_at'),
    })


def postsave(request, pid):
    if request.method == 'POST':
        post = Posts.objects.get(id=pid)
        if post.saved_by.filter(id=request.user.id).exists():
            post.saved_by.remove(request.user)
        else:
            post.saved_by.add(request.user)
    return go_back(request, pid)


def postlike(request, pid):
    if request.method == 'POST':
        post = Posts.objects.get(id=pid)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)     # already liked, so unlike
        else:
            post.likes.add(request.user)
    return go_back(request, pid)


def commentadd(request, pid):
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()[:500]
        if text:
            Comment.objects.create(post_id=pid, user=request.user, text=text)
    return redirect('postview', pid=pid)


def commentdelete(request, cid):
    comment = Comment.objects.get(id=cid)
    pid = comment.post_id
    # the comment's author or the post's owner can delete it
    if request.method == 'POST' and request.user in (comment.user, comment.post.user):
        comment.delete()
    return redirect('postview', pid=pid)


def explore(request):
    q = request.GET.get('q', '').strip()
    posts = (Posts.objects.select_related('user')
             .annotate(like_count=Count('likes', distinct=True),
                       comment_count=Count('comments', distinct=True))
             .order_by('-id'))
    if q:
        posts = posts.filter(
            Q(title__icontains=q) | Q(des__icontains=q) | Q(user__username__icontains=q)
        )
    return render(request, 'explore.html', {
        'posts': posts,
        'q': q,
        'saved_ids': set(Posts.objects.filter(saved_by=request.user).values_list('id', flat=True)),
        'liked_ids': set(Posts.objects.filter(likes=request.user).values_list('id', flat=True)),
    })