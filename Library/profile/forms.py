from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from Library.book_library.models import Book
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions, FieldWithButtons, InlineField, StrictButton


class AskReturnForm(forms.Form):
    def __init__(self, queryset, *args, **kwargs):
        super(AskReturnForm, self).__init__(*args, **kwargs)
        self.fields["choices"] = forms.ModelChoiceField(queryset=queryset, label="Select book to ask")


class ProfileForm(ModelForm):
    first_name=forms.CharField(max_length=30,required=True,widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name=forms.CharField(max_length=30,required=True,widget=forms.TextInput(attrs={'placeholder': 'Last name'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name']

    helper = FormHelper()
    helper.form_class = 'form-signin'
    helper.form_show_labels=False
    helper.layout = Layout(
            Field('first_name'),
            Field('last_name'),
            FormActions(

                    Submit('save_changes_profile', 'Save', css_class='btn btn-lg btn-success'),
                    Submit('cancel_profile', 'Cancel', css_class='btn btn-lg btn-danger '),
                    css_class='btn-group  btn-group-lg form-actions',
                    id='id-action-form-change',

            )
    )


