from django.conf.urls import patterns, url
from views import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/$', ProfileView.as_view(template_name="profile.html",
                                                     )
        ,name='profile'),
    url(r'^(?P<pk>\d+)/change/$', ProfileFormView.as_view(success_url='..',
                                                    template_name="profile_change.html"),
        name='change'),
    url(r'^users/$', UsersView.as_view(template_name='users_list.html',),
        name='all'),

    )