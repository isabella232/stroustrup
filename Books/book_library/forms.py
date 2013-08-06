from django.forms import ModelForm
from models import Book, Book_Tag, Author
from django import forms


class BookForm(ModelForm):

    class Meta:
        model = Book
        fields = ['isbn', 'title', 'e_version_exists', 'paperback_version_exists',
                  'description', 'picture', 'authors', 'tags']


class Book_TagForm(ModelForm):

    class Meta:
        model = Book_Tag
        fields = ['tag','books']


class ChangeBookForm(ModelForm):

    class Meta:
        model = Book
        fields = ['tags', 'authors']


class AuthorForm(ModelForm):

    class Meta:
        model = Author
        fields = ['first_name','last_name','middle_name','books']


class SureForm(forms.Form):
    confirm = forms.BooleanField(label='Are you sure?', required=False)


class SearchForm(forms.Form):
    keywords = forms.CharField(label='Search', max_length=45)