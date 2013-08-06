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
from django import forms

class Client_Story_Record(models.Model):
    book_taken = models.DateField(auto_now_add=True)
    book_returned = models.DateField(auto_now_add=False,blank=True)
    book = models.ForeignKey('Book')
    client = models.ForeignKey('Library_Client')

class Author(models.Model):
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

class Book(models.Model):                                                        #       ,    ,
    isbn = models.BigIntegerField(validators = [MinValueValidator(0), MaxValueValidator(9999999999999)])  # 13 digit ISBN
    title = models.CharField(max_length=45)
    busy = models.BooleanField(default = 0)
    e_version_exists = models.BooleanField(default = 0)
    paperback_version_exists = models.BooleanField(default=True)
    description = models.TextField(max_length=45, default="No description available.")
    picture = models.FileField(upload_to='files', default='No_image_available.svg')
    authors = models.ManyToManyField(Author)
    tags = models.ManyToManyField("Book_Tag", blank=True)
    clients = models.ManyToManyField(Library_Client, through='Client_Story_Record')

    def __unicode__(self):
        return self.title

class Book_Tag(models.Model):
    tag = models.CharField(max_length=20)
    books = models.ManyToManyField(Book)



