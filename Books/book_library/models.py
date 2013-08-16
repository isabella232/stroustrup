import datetime
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator


class Client_Story_Record(models.Model):
    records = models.Manager()

    book = models.ForeignKey('Book')
    user = models.ForeignKey(User)
    book_taken = models.DateTimeField(default=datetime.datetime.now, blank=False)
    book_returned = models.DateTimeField(null=True, blank=True)


class Author(models.Model):
    authors = models.Manager()

    first_name = models.CharField(max_length=45, verbose_name="First name")
    last_name = models.CharField(max_length=45, verbose_name="Last name")

    def __unicode__(self):
        return self.first_name+' '+self.last_name


class Book(models.Model):
    books = models.Manager()

    isbn = models.CharField(help_text="13 digit", max_length=13, blank=True,
                            validators=[RegexValidator(regex="\d{13,13}", message="please just 13 digits")],
                            )
    title = models.CharField(max_length=45)
    busy = models.BooleanField(default=False)
    e_version_exists = models.BooleanField(default=False, verbose_name="e version")
    paperback_version_exists = models.BooleanField(default=True, verbose_name="paper version")
    description = models.TextField(max_length=45, default="No description available.")
    picture = models.FileField(upload_to='book_images', blank=True)
    authors = models.ManyToManyField(Author, symmetrical=True, related_name="books")
    users = models.ManyToManyField(User, symmetrical=True, related_name="books", through=Client_Story_Record, blank=True)
    tags = models.ManyToManyField("Book_Tag", symmetrical=True, related_name="books", blank=True)

    def __unicode__(self):
        return self.title

    def taken_about(self):
        taken = self.client_story_record_set.latest('book_taken').book_taken.date()
        now = datetime.date.today()
        return abs((taken - now).days)

    def taken_by(self):
        if self.busy:
            return self.client_story_record_set.latest('book_taken').user
        return None

    def take_by(self, client):
        self.busy = True
        new_record = Client_Story_Record(book=self, user=client)
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

    tag = models.CharField(max_length=20, unique=True, error_messages={'unique': 'Tag already exists.'})

    def __unicode__(self):
        return self.tag



class Book_Request(models.Model): #SpaT_edition
    requests = models.Manager()

    url = models.URLField(null='')
    title = models.CharField(max_length=30)
    vote = models.IntegerField(default=0)
    def __unicode__(self):
        return self.title






