from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.contrib.auth.views import login
#backends.default.

urlpatterns = patterns('',
                       # url(r'^activate/complete/$',
                       #     TemplateView.as_view(template_name='registration/activation_complete.html'),
                       #     name='activation_complete'),
                       # # Activation keys get matched by \w+ instead of the more specific
                       # # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
                       # # that way it can return a sensible "invalid key" message instead of a
                       # # confusing 404.
                       # url(r'^activate/(?P<activation_key>\w+)/',
                       #     ActivationView.as_view(),
                       #     name='registration_activate'),
                       # url(r'^register/$',
                       #     RegistrationView.as_view(),
                       #     name='register'),
                       # url(r'^register/complete/$',
                       #     TemplateView.as_view(template_name='registration/registration_complete.html'),
                       #     name='complete'),
                       # url(r'^register/closed/$',
                       #     TemplateView.as_view(template_name='registration/registration_closed.html'),
                       #     name='disallowed'),
                       # (r'', include('registration.auth_urls')),
                       url(r'^$', login, {'template_name': 'login.html'}, name='login'),
)