from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Post
from .forms import PostForm
import pudb

# Create your views here.
def index(request):
    # if request.method == 'GET': 
    #     # this line gets all the todos that we have in the db
    #     todos = Todo.objects.all()
    #     # creates them into a context dict
    #     context = {'todos': todos}
    #     # send them all to the db
    return render(request, 'blog/index.html')


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
                "create_post_form": form,
            }
            return render(request, 'blog/create.html', context)
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])




