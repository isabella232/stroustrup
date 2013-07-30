import datetime
import random
import sha

from django.contrib.auth import login
from django.shortcuts import render_to_response,redirect
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.template import loader
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from registration.forms import RegistrationForm
from registration.models import RegistrationProfile
from registration import signals


class _RequestPassingFormView(FormView):
    """
    A version of FormView which passes extra arguments to certain
    methods, notably passing the HTTP request nearly everywhere, to
    enable finer-grained processing.
    
    """
    def get(self, request, *args, **kwargs):
        # Pass request to get_form_class and get_form for per-request
        # form control.
        form_class = self.get_form_class(request)
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        # Pass request to get_form_class and get_form for per-request
        # form control.
        form_class = self.get_form_class(request)
        form = self.get_form(form_class)
        if form.is_valid():
            # Pass request to form_valid.
            return self.form_valid(request, form)
        else:
            return self.form_invalid(form)

    def get_form_class(self, request=None):
        return super(_RequestPassingFormView, self).get_form_class()

    def get_form_kwargs(self, request=None, form_class=None):
        return super(_RequestPassingFormView, self).get_form_kwargs()

    def get_initial(self, request=None):
        return super(_RequestPassingFormView, self).get_initial()

    def get_success_url(self, request=None, user=None):
        return 'registration:complete'

    def form_valid(self, form, request=None):
        return super(_RequestPassingFormView, self).form_valid(form)

    def form_invalid(self, form, request=None):
        return super(_RequestPassingFormView, self).form_invalid(form)


def errorHandle(request, error, error_type, form):
    if error_type=='sign_up_error':
        template = loader.get_template('registration_form.html')
        context = RequestContext(request, {'error': error, 'form': form,} )
        return HttpResponse(template.render(context))
    else:
        template = loader.get_template('unknown_error.html')
        context = RequestContext(request, {'error': error, 'form': form, })
        return HttpResponse(template.render(context))

class RegistrationView(_RequestPassingFormView):
    """
    Base class for user registration views.
    
    """
    disallowed_url = 'registration_disallowed'
    form_class = RegistrationForm
    http_method_names = ['get', 'post', 'head', 'options', 'trace']
    success_url = None
    template_name = 'registration_form.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Check that user signup is allowed before even bothering to
        dispatch or do other processing.
        
        """
        if not self.registration_allowed(request):
            return redirect(self.disallowed_url)
        return super(RegistrationView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, request, form):
        new_user = self.register(request, **form.cleaned_data)
        success_url = self.get_success_url(request, new_user)
        
        # success_url may be a simple string, or a tuple providing the
        # full argument set for redirect(). Attempting to unpack it
        # tells us which one it is.
        try:
            to, args, kwargs = success_url
            return redirect(to, *args, **kwargs)
        except ValueError:
            return HttpResponseRedirect(reverse(success_url, args=()))

    def registration_allowed(self, request):
        """
        Override this to enable/disable user registration, either
        globally or on a per-request basis.
        
        """
        return True

    def register(self, request, **cleaned_data):
        if request.method == 'POST': # If the form has been submitted...
            form = RegistrationForm(request.POST) # A form bound to the POST data
            if form.is_valid():
                email= request.POST['email']
                username = request.POST['username']
                password = request.POST['password1']
                user = User.objects.create_user(username=username, password=password, email=email)
                user.is_active = False
                user.save()
                salt = sha.new(str(random.random())).hexdigest()[:5]
                activation_key = sha.new(salt+user.username).hexdigest()
                key_expires = datetime.datetime.today() + datetime.timedelta(2)
                new_profile = RegistrationProfile.objects.create(user=user,
                                          activation_key=activation_key,
                                          key_expires=key_expires)
                email_subject = 'Your new example.com account confirmation'
                email_body = "Hello, %s, and thanks for signing up for an " \
                             "example.com account!\n\nTo activate your account, click this link within 48 " \
                             "hours:\n\nhttp://example.com/accounts/activate/%s" % (
                    user.username,
                    new_profile.activation_key)
                something = 1
               # send_mail(email_subject, email_body, 'accounts@example.com', [user.email])
            else:
                error = u'form is invalid'
                error_type = 'sign_up_error'
                return errorHandle(request, error, error_type, form)
        else:
            form = RegistrationForm() # An unbound form
            return render_to_response('registration_form.html', {'form': form,},
                                      context_instance = RequestContext(request))

    def send_registration_confirmation(conf_code, email):
        title = "Libary account confirmation"
        content = "http://127.0.0.1/confirm/" + str(conf_code)
        #send_mail(title, content, 'no-reply@gmail.com', email, fail_silently=False)

    def confirm(request, confirmation_code, username):
        try:
            user = User.objects.get(username=username)
            profile = user.get_profile()
            if profile.confirmation_code == confirmation_code and\
                            user.date_joined > (datetime.datetime.now()-datetime.timedelta(days=1)):
                user.is_active = True
                user.save()
                user.backend='django.contrib.auth.backends.ModelBackend'
                login(request,user)
            return HttpResponseRedirect('../../../../../')
        except:
            return HttpResponseRedirect('../../../../../')
                

class ActivationView(TemplateView):
    """
    Base class for user activation views.
    
    """
    http_method_names = ['get']
    template_name = 'activate.html'

    def get(self, request, *args, **kwargs):
        activated_user = self.activate(request, *args, **kwargs)
        if activated_user:
            signals.user_activated.send(sender=self.__class__,
                                        user=activated_user,
                                        request=request)
            success_url = self.get_success_url(request, activated_user)
            try:
                to, args, kwargs = success_url
                return redirect(to, *args, **kwargs)
            except ValueError:
                return HttpResponseRedirect(reverse(success_url, args=()))
        return super(ActivationView, self).get(request, *args, **kwargs)

    def activate(self, request, *args, **kwargs):
        a = RegistrationProfile.objects.all()
        try:
            user = RegistrationProfile.objects.filter(activation_key=kwargs['activation_key'])
        except KeyError:
            raise KeyError
        if user:
            user.is_active = True
            return request

    def get_success_url(self, request, user):
        return 'registration:activation_complete' test change
