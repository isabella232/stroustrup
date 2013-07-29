from django.conf.urls import patterns, include, url
from django.contrib import admin


from Books import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.main_view, name='mainpage'),
    url(r'^google/', include('google_login.urls',namespace="google_login")),
    url(r'^login/', include('login.urls', namespace="login")),
    url(r'^profile/',include('profile.urls', namespace="profile")),
    url(r'^accounts/',include('registration.urls', namespace="registration")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login-complete/$', 'django_openid_auth.views.login_complete', name='openid-complete'),
    url(r'^logout/', 'django.contrib.auth.views.logout', {'next_page': '/',}, name='logout'),
    )