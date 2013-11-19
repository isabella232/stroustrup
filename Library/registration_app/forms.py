from registration.forms import RegistrationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _
from captcha.fields import ReCaptchaField


class CustomRegistrationForm(RegistrationForm):
    password1 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Password"),
                                min_length=8)
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Password (again)"),
                                min_length=8)
    captcha = ReCaptchaField()

    good_domains=['crystalnix.com']

    def clean_email(self):

        email_domain = self.cleaned_data['email'].split('@')[1]
        if not email_domain in self.good_domains:
            raise forms.ValidationError("You must use the domain crystalnix.com.")
            return self.cleaned_data['email']

        existing = User.objects.filter(email__iexact=self.cleaned_data['email'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that email already exists."))
        else:
            return self.cleaned_data['email']





