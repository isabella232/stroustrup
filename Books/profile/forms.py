from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from book_library.models import Book


class AskReturnForm(forms.Form):
    def __init__(self, queryset, *args, **kwargs):
        super(AskReturnForm, self).__init__(*args, **kwargs)
        self.fields["choices"] = forms.ModelChoiceField(queryset=queryset, label="Select book to ask")


class ProfileForm(ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name']