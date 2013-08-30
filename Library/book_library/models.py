import datetime
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator
from django.contrib import auth



class Client_Story_Record(models.Model):
    records = models.Manager()

    book = models.ForeignKey('Book')
    user = models.ForeignKey(User)
    book_taken = models.DateTimeField(auto_now_add=True, blank=False)
    book_returned = models.DateTimeField(null=True, blank=True)


class Author(models.Model):
    authors = models.Manager()

    first_name = models.CharField(max_length=45, verbose_name="First name")
    last_name = models.CharField(max_length=45, verbose_name="Last name")

    def __unicode__(self):
        return self.first_name+' '+self.last_name


class Book_Rating(models.Model): #SpaT_edition
    rating_manager = models.Manager()
    user_owner = models.ForeignKey(User, related_name="rating", default=0, blank=True)
    user_rating = models.FloatField(null = 0, default = 0)
    common_rating = models.FloatField(null = 0, default = 0, blank=True )
    votes = models.IntegerField(null = 0, default = 0, blank=True )

    def __unicode__(self):
        return str('total=' + str(self.common_rating)+ ' by ' + str(self.votes) + ' vote(s)'+';\n'+'current_rate=' +
                   str(self.user_rating) + ' user: ' + self.user_owner.username )




class Book_Comment(models.Model):
    comments = models.Manager()
    sent_time = models.DateField()
    comment = models.CharField(max_length= 255, default='')
    user = models.ForeignKey(User, related_name="comment", default=0, blank=True)
    def __unicode__(self):
        return self.user.username + ": " + self.comment





class Book(models.Model):
    books = models.Manager()

    isbn = models.CharField(help_text="13 digit", max_length=13, blank=True,
                            validators=[RegexValidator(regex="\d{13,13}", message="please just 13 digits")],
                            )
    title = models.CharField(max_length=45)
    busy = models.BooleanField(default=False)
    e_version_exists = models.BooleanField(default=False, verbose_name="e version")
    paperback_version_exists = models.BooleanField(default=True, verbose_name="paper version")
    description = models.TextField(max_length=255, default="No description available.")
    picture = models.FileField(upload_to='book_images', blank=True)
    authors = models.ManyToManyField(Author, symmetrical=True, related_name="books")
    users = models.ManyToManyField(User, symmetrical=True, related_name="books", through=Client_Story_Record, blank=True)
    tags = models.ManyToManyField("Book_Tag", symmetrical=True, related_name="books", blank=True)

    book_rating = models.ManyToManyField('Book_Rating', null=None, default=None, blank=True)#SpaT_eedition
    comments = models.ManyToManyField('Book_Comment', symmetrical=False,  related_name='books', default=None, blank=True) #SpaT_edition

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
        new_record = Client_Story_Record.records.create(book=self, user=client)
        new_record.save()
        client.save()
        return self

    def return_by(self, client):
        self.busy = False
        record = self.client_story_record_set.latest('book_taken')
        record.book_returned = datetime.datetime.now()
        record.save()
        return self

    def common_rating(self):
        if self.book_rating.latest('id'):
            return self.book_rating.latest('id').common_rating
        return 0

    def votes_amount(self):
        if self.book_rating.latest('id'):
            return self.book_rating.latest('id').votes
        return 0


class Book_Tag(models.Model):
    tags = models.Manager()

    tag = models.CharField(max_length=20, unique=True, error_messages={'unique': 'Tag already exists.'})

    def __unicode__(self):
        return self.tag


def get_users_books(self):
    return self.books.filter(client_story_record__book_returned=None)

auth.models.User.add_to_class('get_users_books', get_users_books)



class Book_Request(models.Model): #SpaT_edition
    requests = models.Manager()
    user = models.ForeignKey(User, default=None, blank=True)
    users = models.ManyToManyField(User, related_name="request", default=None, blank=True)
    url = models.URLField(null='')
    title = models.CharField(max_length=30)
    vote = models.IntegerField(default=0)
    def __unicode__(self):
        return self.title + ' ' + self.url