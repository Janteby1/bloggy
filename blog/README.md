# UserLESS Blog

* This weekend you will build a simple blog
* This blog will not have any users

##### Start Up

* Make your virtual environment and start it
* Install the Django Toolbelt
* Start your project
* Start your app
* Migrate? 

##### Your Database

* Make a Post model that has the following fields
	* title
	* content
	* slug
	* created at datetime
	* updated at datetime
* Do you have to migrate again?

##### CRUD AGAIN!

* Alright you guys know the drill. We're going to give our Post app all the crud functionalities. 

##### Extra Models (No not the Calvin Klein / Victoria Secret Kind)

* How do you make your Model forms different between Create and Update?
* Update should be populating the form with the content already in the database
* Below is an example of what my update looks like in my whiskey app

```
def posts_update(req, id=None):

	whiskey = get_object_or_404(Post, id=id)

	update_form = PostForm(instance = whiskey)
	context = {
		"whiskey": update_form,
	}

	# PostForm(data=request.POST)
	return render(req, "posts/update.html", context)
```
* Take a look at the docs and see how you can populate the form with your data


##### Templating Inheritance 

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


##### Luxury Goals

***Beautiful Forms***

* Organize your templates so your forms are not all inline

***Beautiful Everything***

* Use Static Files to apply CSS to your templates

***Extra Bonus***

* We'll be taking a look at this next week but if you want to give it a shot earlier check out how you may write [class based views](https://docs.djangoproject.com/es/1.9/topics/class-based-views/)

