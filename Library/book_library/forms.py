from django.forms import ModelForm
#from Library.book_library.models import Book
from models import Book, Book_Tag, Author, Book_Request, Book_Comment, Book_Rating
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms.fields import FileField
from django.forms.models import save_instance
from django.db.models import Q
from django.contrib.auth import models
from django.core.validators import RegexValidator


class NameField(forms.CharField):

    def to_python(self, value):
        if value:
            value = value.split(',')
            value = [tuple(x.split(None, 2)) for x in value if len(tuple(x.split())) > 1]
        return value

    def validate(self, value):
        if not value:
            raise ValidationError(["Enter first name and last name with namespace. Every author shold be separated by comma from another author. Probably you wrote single (last or first) name."])

class TagField(forms.CharField):

    def to_python(self, value):
        if value:
            value = value.split(',')
            for index in range(len(value)):
                  value[index]= str(value[index])
        return value

class IsbnField(forms.CharField):
    def validate(self, value):
        if value:
            try:
                Book.books.get(isbn= value)
            except Book.DoesNotExist:
                return value
            raise  forms.ValidationError('This ISBN is already taken.')




class BookForm(ModelForm):
    isbn = IsbnField( help_text="13 digit", max_length=13,  required=False)
    authors_names = NameField(max_length=100, label="Add authors full names (to separate use a comma):")
    tag_field = TagField(max_length=50, label = 'Add tags (to separate use a comma):', required=False)

    class Meta:
        model = Book
        exclude = ['busy', 'users', 'authors', 'tags', 'book_rating', 'comments']

    def save(self, commit=True):
        authors = self.cleaned_data['authors_names']
        tags = self.cleaned_data['tag_field']
        book= super(BookForm, self).save(commit)
        book.authors.clear()
        book.tags.clear()
        book.authors.remove( )
        book.tags.remove( )

        for author in authors:
        # all inputs checks to belong to db
        # if such input not exists then it creates
        # otherwise - it just becomes book's one
            fname = author[0]
            lname = author[1]
            new_author = None
            flag = False
            for _author in Author.authors.all():
                if _author.first_name == fname and _author.last_name == lname:
                    new_author = _author
                    flag = True
                    break
            if not flag:
                new_author, created = Author.authors.get_or_create(first_name=author[0], last_name=author[1])
            book.authors.add(new_author)





        for _tag in tags:
        #as same as authors
            new_tag = None
            flag = False
            for el in Book_Tag.tags.all():
                if el.tag == _tag:
                    flag = True
                    new_tag = el
                    break
            if not flag:
                new_tag, created = Book_Tag.tags.get_or_create(tag=_tag)
            book.tags.add(new_tag)

        return book


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

    def save(self, commit=True):   #Probably it's became useless
        if self.cleaned_data['url'] and self.cleaned_data['title']:
            _url=self.cleaned_data['url']
            _title=self.cleaned_data['title']
            req = Book_Request.requests.create(url=_url, title=_title)
            req.save()
            return req
        else:
            return super(Book_RequestForm, self).save(commit=True)

class Book_RatingForm(ModelForm):

    class Meta:
        model = Book_Rating

class Book_CommentForm(ModelForm):

    class Meta:
        model = Book_Comment
        fields = ['comment']
