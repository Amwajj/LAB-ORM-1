from django.shortcuts import render ,redirect
from django.http import HttpRequest
from django.utils import timezone
from .models import Post

# Create your views here.

def home_view(request:HttpRequest):
    posts=Post.objects.all().order_by('-published_at')
    return render(request,"post/home.html", {"posts":posts})


def add_post_view(request:HttpRequest):
    if request.method =="POST":
        is_published = request.POST.get("is_published")=="True"
        new_post = Post(title=request.POST["title"],content=request.POST["content"],is_published=is_published,poster=request.FILES["poster"], published_at=timezone.now())
        new_post.save()
        return redirect("post:home_view")
    return render(request,"post/create.html")

def post_detail_view(request:HttpRequest, post_id:int):
    post=Post.objects.get(pk=post_id)
    return render(request,"post/details.html", {"post":post})


def post_update_view(request:HttpRequest, post_id:int):
    post=Post.objects.get(pk=post_id)
    if request.method =="POST":
        post.title = request.POST["title"]
        post.content = request.POST["content"]
        post.is_published = request.POST["is_published"]
        if "poster" in request.FILES:
            post.poster=request.FILES["poster"]
        post.save()
        return redirect("post:post_detail_view", post_id=post.id)
    return render(request,"post/update.html", {"post":post})

def post_delete_view(request:HttpRequest, post_id:int):
    post=Post.objects.get(pk=post_id)

    post.delete()

    return redirect("post:home_view")