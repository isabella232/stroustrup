from django.conf.urls import patterns, url
import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.profile,name='profile'),
    url(r'^change/$', views.profile_change,name='change'),
    )