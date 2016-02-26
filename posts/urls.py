from django.conf.urls import patterns, include, url
from django.contrib import admin
from posts import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
    url(r'^create$', views.create, name="create"),

    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
)