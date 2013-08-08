from django.forms import ModelForm
from models import Book, Book_Tag, Author
from django import forms


class BookForm(ModelForm):

    class Meta:
        model = Book
        exclude = ['busy', 'users']


class Book_TagForm(ModelForm):

    class Meta:
        model = Book_Tag


class AuthorForm(ModelForm):

    class Meta:
        model = Author


class SureForm(forms.Form):
    confirm = forms.BooleanField(label='Are you sure?', required=False)


class SearchForm(forms.Form):
    busy = forms.NullBooleanField(label="Busy")
    keywords = forms.CharField(label="Search", max_length=45, required=False)