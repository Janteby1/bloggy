from django.conf.urls import patterns, include, url
from django.contrib import admin
from posts import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
    url(r'^create$', views.create, name="create"),
    url(r'^edit/(?P<post_id>[0-9]+)$', views.edit, name="edit"),
)