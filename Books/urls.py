from django.conf.urls import patterns, include, url
from django.contrib import admin
from django_openid_auth.views import login_complete
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from book_library.views import UsersView

dajaxice_autodiscover()


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

                       (r'^books/', include('book_library.urls', namespace='books')),
                       url(r'^users/$', UsersView.as_view(template_name='book_library/users_list.html',),),
                       url(r'^auth/', include('registration.auth_urls', namespace="authorisation")),
                       url(dajaxice_config.dajaxice_url, include('dajaxice.urls'),)
                       )

urlpatterns += staticfiles_urlpatterns()