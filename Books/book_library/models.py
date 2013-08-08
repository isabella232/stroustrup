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
import datetime


class Client_Story_Record(models.Model):
    records = models.Manager()

    book = models.ForeignKey('Book')
    client = models.ForeignKey('Library_Client')
    book_taken = models.DateTimeField(default=datetime.datetime.now, blank=False)
    book_returned = models.DateTimeField(null=True, blank=True)


class Author(models.Model):
    authors = models.Manager()

    first_name = models.CharField(max_length=45, verbose_name="First name")
    last_name = models.CharField(max_length=45, verbose_name="Last name")
    middle_name = models.CharField(max_length=45, blank=True)

    def __unicode__(self):
        return self.first_name+' '+self.last_name


class Book(models.Model):
    books = models.Manager()
                                               #       ,    ,
    isbn = models.BigIntegerField(validators=[MinValueValidator(1000000000000)], max_length=13, blank=True, null=True)  # 13 digit ISBN
    title = models.CharField(max_length=45)
    busy = models.BooleanField(default=False)
    e_version_exists = models.BooleanField(default=False, verbose_name="e version")
    paperback_version_exists = models.BooleanField(default=True, verbose_name="paper version")
    description = models.TextField(max_length=45, default="No description available.")
    picture = models.FileField(upload_to='book_images', blank=True)
    authors = models.ManyToManyField(Author, related_name="books")
    tags = models.ManyToManyField("Book_Tag", related_name="books")

    def __unicode__(self):
        return self.title

    def take_by(self, client):
        self.busy = True
        new_record = Client_Story_Record(book=self, client=client)
        new_record.save()
        client.save()
        return self

    def return_by(self, client):
        self.busy = False
        record = self.client_story_record_set.latest('book_taken')
        record.book_returned = datetime.datetime.now()
        record.save()
        return self


class Library_Client(models.Model):
    clients = models.Manager()

    books = models.ManyToManyField(Book, blank=True, through=Client_Story_Record)
    user = models.OneToOneField(User, primary_key=True)

    def __unicode__(self):
        return self.user.first_name+' '+self.user.last_name


class Book_Tag(models.Model):
    tags = models.Manager()

    tag = models.CharField(max_length=20, primary_key=True)

    def __unicode__(self):
        return self.tag






