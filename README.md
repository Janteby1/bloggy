# Intermediate Django stuff

### Learning Objectives
***Students will be able to...***

* Add a custom save method to a Model
* Use more advanced Django queries
* Catch errors on Model forms
* Reuse a model form in multiple views
* Use template inheritance
* Use staticfiles in Django

---
### Context

* Continuing to become Full Stack Developers

---
### Lesson

####Part 0 - Add a custom save method to a Model

#####**Our old model**
Yesterday, we had a model that looked like this:
```
from django.db import models

# Create your models here.

class Todo(models.Model):
    description = models.CharField(max_length=30)
    created_at = models.DateField(auto_now=True)
    completed = models.BooleanField(default=False)
```

But today, we're going to be working with making blogs in Django. When making blogs, a `slug` is helpful. (Why? Read here: [http://stackoverflow.com/questions/427102/what-is-a-slug-in-django](http://stackoverflow.com/questions/427102/what-is-a-slug-in-django)). Let's look at how we can edit our model to incorporate a slug:

```
...
from django.utils.text import slugify

class Post(models.Model):
    title = models.CharField(max_length=40)
    content = models.CharField(max_length=4000)
    slug = models.SlugField(max_length=40)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.updated_at = timezone.now()
        if not self.id:
            self.created_at = timezone.now()
        super(Post, self).save(*args, **kwargs)
```

####Part 1 - Use more advanced Django queries

So far, we know how to do something like this for queries:
```
todos = Todo.objects.all()
```
or like this:
```
todo = Todo.objects.get(pk=3)
```
Now, what if we wanted to change the order that Django returns the items to us from the database? We could do something like this:
```
all_posts = Post.objects.all().order_by('-updated_at')
```
This would give us all the Post objects from the database, but it would return them in reverse order of when they were updated.

####Part 2 - Catch errors on Model forms

If we have an error in a model form submission, we should catch that error and return some sort of error message to the user. We can do that like this:
```
def edit(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("blog:index")
        else:
            context = {
                "post": post,
                "edit_post_form": form,
            }
            return render(request, "blog/edit.html", context)
```
In this example, if the form is valid, Django will save it to the db and redirect the user. If the form is not valid (ie. there's errors), then Django will attach those errors to the form object. We can return that form object to the user so that the template can display those errors for the user. How might be setup our template to should those errors?

We could use something like this:

```
<form action="{% url 'blog:edit' id=post.id %}" method="POST">
    {% csrf_token %}

    {% for field in edit_post_form %}
        <div class="{%if field.errors %}error{%endif%}">
            {{field.label_tag}}{{ field }}
        </div>
        {% for error in field.errors %}
            <small class="error">{{ error }}</small>
        {% endfor %}
    {% endfor %}

    <input type="submit" class="button" value="Edit Post" />
</form>
```
Notice that `"{% url 'blog:edit' id=post.id %}"` section of line 1 in this code block? What do you think that does?

That gets a URL with a route like this:
```
url(r'^edit/(?P<id>[0-9]+)$', blog.views.edit, name='edit')
```

Which then calls a view with a name like,
```
def edit(request, id)
```

Also notice how we're iterating across the fields in our form. We can do this with Django model forms! This allows us to add places for the form to display our errors. It also allows us to add CSS classes and styling to our form fields.

CAUTION: Do not copy/paste the above template example. You should come up with your own soluton! You learn nothing by copy/pasting others code!

####Part 3 - Reuse a model form in multiple views

Yesterday, we had two forms, like this:
```
class NewTodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = [
            "description",
        ]

class UpdateTodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = [
            "description",
            "completed",
        ]
```
But, they pretty much did the same things. Presumably, we could just make one form, like this:
```
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
        ]
```
Then, when we use it in a `create` route, we could do something like this:
```
form = PostForm()
```
To make an empty version of it. And if I use this model form in an `update` route, I could do something like this:
```
form = PostForm(instance=post)
```
And this would allow me to prepopulate that form with the post data.
####Part 4 - Use template inheritance
* Now that you built out all your views / url files / and template files lets work on template inheritance
* Here's a review of what we did in class
* First make a `base.html` file in templates
    * This file will hold your base html information.
    * It will also have a section that will act dynamically and be pre populated with other templates

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>WHISKEYS</title>
</head>
<body>

    <h1>THIS HEADER WILL ALWAYS SHOW UP NO MATTER WHAT URL ENDPOINT THE USER GOES TO</h1>

    <div class=container>
        {% block content %}

        {% endblock content %}
    </div>

</body>
</html>
```
* Below is an example of how we will connect a template to the base

```
{% extends "posts/base.html" %}

{% block content %}

    {% for whiskey in whiskey_list %}
        <ul>
            <h3><a href="{{whiskey.id}}">{{whiskey.brand}}</a></h3>
            <li>{{whiskey.brand_type}}</li>
            <li>{{whiskey.price}}</li>
            <p>{{whiskey.description}}</p>
        </ul>


    {% endfor %}

{% endblock content %}
```
* The first line says "extend" this content to `posts/base.html` file when it is called. (this path may be different if you have it in a different folder in templates)
* Use the `block content` templating to replace the `block content` in the base file

####Part 5 - Use staticfiles in Django
When we use static files in Django (like `css` or `javascript` files), we need to do a little work to get everything configured correctly. First, we need to create a `static` directory within our app, so that our project looks like this:

```
my_jeff_rules/
    manage.py
    posts/
        static/
        templates/
        __init__.py
        admin.py
        models.py
        tests.py
        views.py
    blog/
        __init__.py
        settings.py
        urls.py
        wsgi.py
```
Notice the `static/` directory that I've created within my app folder. Then, we can use this syntax to serve our `static` files:
```
<!DOCTYPE html>
{% load staticfiles %}
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Bloggy: A Blog about Blogs</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/foundation/5.5.2/css/foundation.css" />
    <link rel="stylesheet" type="text/css" href="{% static 'blog/style.css' %}" />
</head>
<body>
```
Notice:
```
{% load staticfiles %}
```
and
```
<link rel="stylesheet" type="text/css" href="{% static 'blog/style.css' %}" />
```
{% load staticfiles %} loads the {% static %} template tag from the staticfiles template library. The {% static %} template tag generates the absolute URL of the static file.

For more of an explanation about how `staticfiles` in Django works, read here:

 - https://docs.djangoproject.com/en/1.9/howto/static-files/
 - https://docs.djangoproject.com/en/1.9/ref/settings/#std:setting-STATICFILES_FINDERS

