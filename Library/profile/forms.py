from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from Library.book_library.models import Book
from Library.profile.models import Profile_addition
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions, FieldWithButtons, InlineField, StrictButton
from django.forms.formsets import formset_factory


class AskReturnForm(forms.Form):
    def __init__(self, queryset, *args, **kwargs):
        super(AskReturnForm, self).__init__(*args, **kwargs)
        self.fields["choices"] = forms.ModelChoiceField(queryset=queryset, label="Select book to ask")


class ProfileForm(ModelForm):
    first_name=forms.CharField(max_length=30,required=True,widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name=forms.CharField(max_length=30,required=True,widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    email=forms.EmailField(required=True,widget=forms.TextInput(attrs={'placeholder': 'E-mail'}))
    avatar = forms.ImageField(widget=forms.ClearableFileInput(attrs={'placeholder': 'Avatar'}), required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name','email']

    helper = FormHelper()
    helper.form_class = 'form-signin'
    helper.form_show_labels=False
    helper.layout = Layout(
            Field('first_name'),
            Field('last_name'),
            Field('email'),
            Field('avatar',wrapper_class='form-control'),
            FormActions(

                    Submit('save_changes_profile', 'Save', css_class='btn btn-lg btn-success'),
                    Submit('cancel_profile', 'Cancel', css_class='btn btn-lg btn-danger '),
                    css_class='btn-group  btn-group-lg form-actions',
                    id='id-action-form-change',

            )
    )

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        if not self.is_bound and self.instance.pk:
            profile = self.instance.profile_addition_set.latest('id')
            self.fields['avatar'].initial = profile.avatar

    def save(self, commit=True):
        profile = super(ProfileForm, self).save(commit)
        photo = self.cleaned_data['avatar']
        if photo is None:
            return profile

        if photo is False:
            photo=None

        new_avatar, created = Profile_addition.objects.get_or_create(defaults={'avatar':photo},user_id=profile.pk)
        if created is False:
                new_avatar.avatar = photo
                new_avatar.save()
        return profile

class ProfileFormAddition(ModelForm):

    class Meta:
        model= Profile_addition


