from registration.forms import RegistrationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _
from captcha.fields import ReCaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions, FieldWithButtons, InlineField, StrictButton
from django.contrib.auth.forms import AuthenticationForm


class CustomRegistrationForm(RegistrationForm):
    password1 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Password"),
                                min_length=8)
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Password (again)"),
                                min_length=8)
    captcha = ReCaptchaField()

    good_domains=['crystalnix.com']

    helper = FormHelper()
    helper.form_class = 'form-signin'
    helper.form_method = 'POST'
    helper.layout = Layout(
            Field('username'),
            Field('email'),
            Field('password1'),
            Field('password2'),
            Field('captcha'),
            Submit('sign_up', 'Sign up!', css_class='btn btn-lg btn-block btn-success')
            )

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


class CustomAuthForm(AuthenticationForm):

    helper = FormHelper()
    helper.form_class = 'form-signin'
    helper.form_method = 'POST'
    error_text_inline = True
    helper.layout = Layout(
                'username',
                'password',
                FormActions(
                                Submit('sign_in_auth', 'Sign in!', css_class='btn btn-lg btn-block btn-primary'),
                           )
    )

