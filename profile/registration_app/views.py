from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect

from profile.registration_app.forms import LandingForm


class LandingPage(FormView):
    form_class = LandingForm
    success_url = '/thanks/'

    def form_valid(self, form):
        email = self.request.POST['email']
        mail = 'Hello, Please contact him.\n'+ email
        staff = User.objects.filter(is_staff=True)
        email_list = []
        for user in staff:
            email_list.append(user.email)
        send_mail('New User', mail, email, email_list, fail_silently=False)
        return redirect(self.get_success_url())


