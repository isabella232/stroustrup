from django.forms import ModelForm
from models import Book, Book_Tag, Author, Book_Request
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms.fields import FileField
from django.forms.models import save_instance
from django.db.models import Q
from django.contrib.auth import models

class NameField(forms.CharField):

    def validate(self, value):
        strings = value.split(' ')
        if len(strings) > 1:
            fname = strings[0]
            lname = strings[1]
            filter = Q(first_name__iexact=fname) &\
                         Q(last_name__iexact=lname)
            if Author.authors.filter(filter):
                raise ValidationError(["Author already exists."])



class BookForm(ModelForm):
    author_name = NameField(max_length=90, required=False, label="Add authors full names (to seprate use a comma):")
    tag = forms.CharField(max_length=90, required = False, label = 'Add tags (to separate use a comma):')
    authors = forms.ModelMultipleChoiceField(queryset=Author.authors.all(), required=False, label="Authors")

    class Meta:
        model = Book
        exclude = ['busy', 'users']

    def save(self, commit=True):
        if self.cleaned_data['tag']:
            strings=self.cleaned_data['tag'].split(',')
            for string in strings:
                tag=Book_Tag.tags.create(tag = string)
                book = super(BookForm, self).save(commit=True)
                book.tags.add(tag)
                book.save()

        if self.cleaned_data['author_name']:
            strings = self.cleaned_data['author_name'].split(',')
            for string in strings:
                string = string.split(' ')
                fname = string[0]
                lname = string[1]
                author = Author.authors.create(first_name=fname, last_name=lname)
                book = super(BookForm, self).save(commit=True)
                book.authors.add(author)
                book.save()


        return super(BookForm, self).save(commit=True)


class Book_TagForm(ModelForm):

    class Meta:
        model = Book_Tag


class AuthorForm(ModelForm):

    class Meta:
        model = Author


class SureForm(forms.Form):
    confirm = forms.BooleanField(label='Are you sure?', required=False)


class SearchForm(forms.Form):
    busy = forms.BooleanField(label='Busy', required=False)
    free = forms.BooleanField(label='Free', required=False)
    keywords = forms.CharField(label="Search", max_length=45, required=False)

class Book_RequestForm(ModelForm): #SpaT_edition


    class Meta:
        model = Book_Request
        fields = ['title', 'url']

    def save(self, commit=True):
        if self.cleaned_data['url'] and self.cleaned_data['title']:
            _url=self.cleaned_data['url']
            _title=self.cleaned_data['title']

            req = Book_Request.requests.create(url=_url, title=_title)

            req.save()
            return req

        else:
            return super(Book_RequestForm, self).save( commit=True)