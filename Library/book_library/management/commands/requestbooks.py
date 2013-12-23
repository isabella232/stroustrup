__author__ = 'romanusynin'
from Library.book_library.models import Book, Client_Story_Record, Request_Return
from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from Library.main import settings
from datetime import datetime, timedelta
from django.core.mail import send_mail, EmailMessage


class Command(NoArgsCommand):


        def handle(self, *args, **options):
            DEAD_LINE = 14 #days
            query = Request_Return.objects.order_by('id')
            for request_return in query:
                    book = request_return.book
                    if book.taken_about() is DEAD_LINE: #Send email
                        authors_string = ""
                        for author in book.authors.all():
                            authors_string += author.__unicode__()+","
                        user = book.taken_by()
                        server_email = settings.EMAIL_HOST_USER
                        email = EmailMessage('Book return request',
                                             "We is asking you to return the book "+book.title+"  author(s):"+authors_string+
                                             "You can return it by click on this link: "+settings.DOMAIN+"/books/"+str(book.id), #need to modify
                                             server_email,
                                             [user.email]
                                            )
                        email.send()
                    else:
                        self.stdout.write('\nFalse!!!' ,ending='') #need to modify


