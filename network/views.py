from django.contrib.auth import authenticate, login, logout, get_user
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from pytz import utc
from .forms import NewPostForm
from pprint import pprint
from .models import User, Post, Like, Comment



def index(request):
    context = {}
    posts = Post.objects.all()
    posts = posts.order_by("-timestamp").all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    if page_number == None:
        page_number = 1
    page_obj = paginator.page(page_number)
    context["page"] = page_obj
    context["newPostForm"] = NewPostForm
    if get_user(request).is_authenticated:
        context["liked_posts"] = User.objects.get(username=get_user(request)).liked_posts.all()
    return render(request, "network/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("network:index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("network:index"))
    else:
        return render(request, "network/register.html")


@login_required
def add_post(request):
    print("got here")
    print(datetime.now())
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data["body"]
            post = Post.objects.get(id=request.POST.get("id"))
            if post:
                post.body = body
            else:
                post = Post(
                    author = get_user(request),
                    body=body,
                    timestamp=utc.localize(datetime.utcnow())
                )
            post.save() 
    return HttpResponseRedirect(reverse("network:index"))
    

# @login_required
# def profile(request, username):
#     user = User.objects.get(username=username)
#     to_follow = None
#     if user != get_user(request):
#         to_follow = True if len(user.followers.filter(username=get_user(request))) == 0 else False
    
#     user = user.serialize()
#     user["toFollow"] = to_follow
#     return JsonResponse(user)   


@login_required
def posts(request):
    posts = Post.objects.all()
    posts = posts.order_by("-timestamp").all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return JsonResponse([post.serialize() for post in page_obj], safe=False)


@login_required
def user_posts(request, username):
    context = {}
    user = User.objects.get(username=username)
    to_follow = None
    if user != get_user(request):
        to_follow = "Follow" if len(user.followers.filter(username=get_user(request))) == 0 else "Unfollow"
    else:
        to_follow = None
    context["user_details"] = user.serialize()
    context["to_follow"] = to_follow

    posts = Post.objects.all().filter(author=user)
    posts = posts.order_by("-timestamp").all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    if page_number == None:
        page_number = 1
    page_obj = paginator.page(page_number)
    context["page"] = page_obj
    context["username"] = user.username
    return render(request, "network/profile.html", context)


@login_required
def follow_user(request, user_to_follow):
    if request.method == "GET":
        return HttpResponse("POST request only!")
    current_user = User.objects.get(username=get_user(request))
    user_to_follow = User.objects.get(username=user_to_follow)
    try:
        current_user.following.get(username=user_to_follow)
        current_user.following.remove(user_to_follow)
        user_to_follow.followers.remove(current_user)
        print("its ok")
    except Exception:
        current_user.following.add(user_to_follow)
        user_to_follow.followers.add(current_user)
        
    return HttpResponseRedirect(reverse("network:profile", kwargs={'username':user_to_follow}))


@login_required
def following_view(request):
    user = get_user(request)
    following_users = user.following.all()
    following_posts = []
    context = {}
    for following_user in following_users:
        following_posts.extend(Post.objects.all().filter(author=following_user))

    # following_posts = [post.serialize() for post in following_posts]
    paginator = Paginator(following_posts, 10)
    page_number = request.GET.get('page')
    if page_number == None:
        page_number = 1
    page_obj = paginator.page(page_number)
    context["page"] = page_obj
    return render(request, "network/index.html", context)


@login_required
def like(request, post_id):
    context = {
        
    }
    post = Post.objects.get(id=post_id)
    user = get_user(request)
    if post in user.liked_posts.all():
        user.liked_posts.remove(post)
        post.like_counter -=1
        nextBtn = "Like"
    else:
        user.liked_posts.add(post)
        post.like_counter += 1
        nextBtn = "Unlike"

    post.save()
    user.save()

    return JsonResponse({
        "message":"Successfuly liked",
        "currentCounter":post.like_counter,
        "buttonContent":nextBtn
    })