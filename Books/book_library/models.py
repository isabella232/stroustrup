import datetime
import hashlib
import random
import re

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db import transaction
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from settings import STATIC_ROOT, MEDIA_ROOT


class Client_Story_Record(models.Model):
    book_taken = models.DateField(auto_now_add=True)
    book_returned = models.DateField(auto_now_add=False,blank=True)
    book = models.ForeignKey('Book')
    client = models.ForeignKey('Library_Client')


class AuthorManager(models.Manager):

    def create_new_author(self, cleaned_data):
        author = Author()
        author.first_name = cleaned_data['first_name']
        author.last_name = cleaned_data['last_name']
        author.middle_name = cleaned_data['middle_name']
        author.save()
        for book in cleaned_data['books']:
            author.books.add(book)
            book.authors.add(author)
        return author


class Author(models.Model):
    objects = AuthorManager()

    first_name = models.CharField(max_length=45, verbose_name="First name")
    last_name = models.CharField(max_length=45, verbose_name="Last name")
    middle_name = models.CharField(max_length=45, blank=True)
    books = models.ManyToManyField('Book', blank=True)

    def __unicode__(self):
        return self.first_name+' '+self.last_name


class Library_Client(models.Model):
    first_name = first_name = models.CharField(max_length=45, verbose_name="First name")
    last_name = models.CharField(max_length=45, verbose_name="Last name")
    middle_name = models.CharField(max_length=45, blank=True)
    books = models.ManyToManyField('Book', through='Client_Story_Record')

    def __unicode__(self):
        return self.first_name+' '+self.last_name


class BookManager(models.Manager):

    # def author_filter(self, ):
    #     ratings = self.filter(event__in=[event.id for event in events],
    #                           user=user)
    #     rating_dict = collections.defaultdict(lambda: None)
    #     for rating in ratings:
    #         rating_dict[rating.event_id] = rating
    #     return rating_dict


    def create_new_book(self, cleaned_data):
        book = Book()
        book = Book(isbn=cleaned_data['isbn'],
                    title=cleaned_data['title'],
                    e_version_exists=cleaned_data['e_version_exists'],
                    paperback_version_exists=cleaned_data['paperback_version_exists'],
                    description=cleaned_data['description'],
                    picture=cleaned_data['picture'],
                    )
        book.save()
        for author in cleaned_data['authors']:
            book.authors.add(author)
            author.books.add(book)
        for tag in cleaned_data['tags']:
            book.tags.add(tag)
            tag.books.add(book)
        return book


class Book(models.Model):
    books = BookManager()
                                               #       ,    ,
    isbn = models.BigIntegerField(validators=[MinValueValidator(1000000000000)], max_length=13, unique=True)  # 13 digit ISBN
    title = models.CharField(max_length=45)
    busy = models.BooleanField(default = 0)
    e_version_exists = models.BooleanField(default=0, verbose_name="e version")
    paperback_version_exists = models.BooleanField(default=True,verbose_name="paper version")
    description = models.TextField(max_length=45, default="No description available.")
    picture = models.FileField(upload_to='files', default=STATIC_ROOT+"/No_image_Avaliable.gif")
    authors = models.ManyToManyField(Author, related_name="authors")
    tags = models.ManyToManyField("Book_Tag", blank=True)
    clients = models.ManyToManyField(Library_Client, through='Client_Story_Record')

    def __unicode__(self):
        return self.title

    def change(self, cleaned_data):
        book = self
        for author in cleaned_data['authors']:
            book.authors.add(author)
            author.books.add(book)
        for tag in cleaned_data['tags']:
            book.tags.add(tag)
            tag.books.add(book)
        return book


class Book_TagManager(models.Manager):

    def create_new_tag(self, cleaned_data):
        tag = Book_Tag()
        tag.tag = cleaned_data['tag']
        tag.save()
        for book in cleaned_data['books']:
            tag.books.add(book)
            book.tags.add(tag)
        return tag


class Book_Tag(models.Model):
    tags = Book_TagManager()

    tag = models.CharField(max_length=20, primary_key=True)
    books = models.ManyToManyField(Book, blank=True)

    def __unicode__(self):
        return self.tag






