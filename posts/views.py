from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Post
from .forms import PostForm
import pudb

# Create your views here.
def index(request):
    if request.method == 'GET': 
        # this line gets all the todos that we have in the db
        posts = Post.objects.all().order_by('-updated_at')
        # creates them into a context dict
        context = {'posts': posts}
        # send them all to the db
    return render(request, 'blog/index.html', context)

def create(request):
    # pu.db
    # post = get_object_or_404(Post, id=id)
    if request.method == "GET":
        form = PostForm()
        context = {
            "PostForm": form }
        return render (request, "blog/create.html", context)

    elif request.method == "POST":
        form = PostForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("posts:index")
        else:
            context = {
                # "post": post,
                "PostForm": form,
            }
            return render(request, 'blog/create.html', context)
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


def edit(request, post_slug):
    # pu.db
    post = Post.objects.get(slug=post_slug)
    # post = get_object_or_404(Post, id=id)
    if request.method == "GET":
        form = PostForm(instance =post)
        context = {
            "post": post,
            "EditForm": form,
        }
        return render (request, "blog/edit.html", context)

    elif request.method == "POST":
        form = PostForm(data=request.POST, instance =post)
        if form.is_valid():
            form.save()
            return redirect("posts:index")
        else:
            context = {
                "post": post,
                "EditForm": form,
            }
            return render(request, 'blog/edit.html', context)
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


def delete (request, post_slug):
    # this syntax is if we want to delete a post 
    if request.method == 'POST':
        post = Post.objects.get(slug=post_slug)
        post.show = False
        post.save()
        return redirect('posts:index')







