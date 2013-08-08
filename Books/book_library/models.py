import datetime
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator


class Client_Story_Record(models.Model):
    records = models.Manager()

    book = models.ForeignKey('Book')
    client = models.ForeignKey(User)
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
    users = models.ManyToManyField(User, related_name="books", through=Client_Story_Record, blank=True)
    tags = models.ManyToManyField("Book_Tag", related_name="books", blank=True)

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


class Book_Tag(models.Model):
    tags = models.Manager()

    tag = models.CharField(max_length=20, primary_key=True)

    def __unicode__(self):
        return self.tag






