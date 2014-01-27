import os

from django.conf.urls import patterns, url, include
from django.views.generic.base import TemplateView
from registration.backends.default.views import RegistrationView, ActivationView
from profile.registration_app.forms import CustomRegistrationForm, CustomChangePassForm

os.environ['RECAPTCHA_TESTING'] = 'True'


urlpatterns = patterns('',
                       url(r'^activate/complete/$',
                           TemplateView.as_view(template_name='templates/registration/activation_complete.html'),
                           name='registration_activation_complete'),
                       # Activation keys get matched by \w+ instead of the more specific
                       # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
                       # that way it can return a sensible "invalid key" message instead of a
                       # confusing 404.
                       url(r'^activate/(?P<activation_key>\w+)/$',
                           ActivationView.as_view(),
                           name='registration_activate'),
                       url(r'^register/$',
                           RegistrationView.as_view(form_class=CustomRegistrationForm),
                           name='registration_register'),
                       url(r'^register/complete/$',
                           TemplateView.as_view(template_name='templates/registration/registration_complete.html'),
                           name='registration_complete'),
                       url(r'^register/closed/$',
                           TemplateView.as_view(template_name='registration/registration_closed.html'),
                           name='registration_disallowed'),
                       url(r'^password/change/$', 'django.contrib.auth.views.password_change',
                           {'password_change_form':CustomChangePassForm, 'template_name': 'templates/registration/password_change.html'},
                           name='password_change' ),
                       url(r'^password/change/done/$', TemplateView.as_view(template_name='templates/registration/pass_change_done.html'),
                           name='auth_password_change_done' ),
                       (r'', include('registration.auth_urls')),

                       )