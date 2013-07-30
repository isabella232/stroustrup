from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

from registration.views import ActivationView, RegistrationView

urlpatterns = patterns('',
                       url(r'^activate/complete/$',
                           TemplateView.as_view(template_name='activation_complete.html'),
                           name='activation_complete'),
                       url(r'^activate/wrong_key/$',
                           TemplateView.as_view(template_name='activate.html'),
                           name='activate'),
                       # Activation keys get matched by \w+ instead of the more specific
                       # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
                       # that way it can return a sensible "invalid key" message instead of a
                       # confusing 404.
                       url(r'^activate/(?P<activation_key>\w+)/',
                           ActivationView.as_view(),
                           name='registration_activate'),
                       url(r'^register/$',
                           RegistrationView.as_view(),
                           name='register'),
                       url(r'^register/complete/$',
                           TemplateView.as_view(template_name='registration_complete.html'),
                           name='complete'),
                       url(r'^register/closed/$',
                           TemplateView.as_view(template_name='registration_closed.html'),
                           name='disallowed'),
                       (r'', include('registration.auth_urls')),
                       )