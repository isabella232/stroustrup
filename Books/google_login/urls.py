from django.conf.urls import patterns, url
from django.contrib import admin
from django_openid_auth import views
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^login/$', 'django_openid_auth.views.login_begin', name='openid-login'),
                       url(r'^login-complete/$', 'django_openid_auth.views.login_complete', name='openid-complete'),
)