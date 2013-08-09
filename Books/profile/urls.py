from django.conf.urls import patterns, url
import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/$', views.ProfileView.as_view(success_url='.',
                                                     template_name="profile.html",
                                                     )
        ,name='profile'),
    url(r'^(?P<pk>\d+)/change/$', views.ProfileFormView.as_view(success_url='..',
                                                    template_name="profile_change.html"),
        name='change'),
    )