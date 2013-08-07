from django.conf.urls import patterns, include, url
from django.contrib import admin
from django_openid_auth.views import login_complete

import views,settings

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', views.main_view, name='mainpage'),

                       url(r'^openid/login/$', 'django_openid_auth.views.login_begin', name='openid-login'),
                       url(r'^openid/login-complete/$', login_complete, name='openid-complete'),

                       url(r'^profile/',include('profile.urls', namespace="profile")),
                       (r'^accounts/', include('registration_app.urls')),

                       (r'^books/', include('book_library.urls',namespace='books')),

                       (r'^auth/', include('registration.auth_urls', namespace="authorisation")),
                       )