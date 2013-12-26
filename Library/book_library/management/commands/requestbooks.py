__author__ = 'romanusynin'
from Library.book_library.models import Book, Client_Story_Record, Request_Return
from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from Library.main import settings
from datetime import datetime, timedelta
from django.core.mail import send_mail, EmailMessage


class Command(NoArgsCommand):


        def handle(self, *args, **options):
            DEADLINE = 14 #days
            query = Request_Return.objects.order_by("book__id", "id").distinct('book')
            for request_return in query:
                    book = request_return.book
                    authors = u", ".join(unicode(v) for v in book.authors.all())
                    server_email = settings.EMAIL_HOST_USER
                    if book.busy == False :
                        user = request_return.user_request
                        email = EmailMessage('Book free request',
                                             "Book (''"+book.title+"'' author(s): " + authors + " ) has been returned."
                                             " You can take it by click on this link: "+settings.DOMAIN+"/books/"
                                             + str(book.id), #need to modify
                                             server_email, [user.email])
                        email.send()
                        request_return.delete()
                        continue
                    if request_return.processing_time!=None:
                        round_day=datetime.now() - request_return.processing_time
                    if book.taken_about() is DEADLINE and (request_return.processing_time is None or round_day.days>0): #Send email
                        user = book.taken_by()
                        email = EmailMessage('Book return request',
                                             "We is asking you to return the book: ''"+book.title+"'' author(s): "
                                             + authors +
                                             " You can return it by click on this link: "+settings.DOMAIN+"/books/"
                                             + str(book.id), #need to modify
                                             server_email, [user.email])
                        email.send()
                        request_return.processing_time = datetime.now()
                        request_return.save()
                    else:
                        self.stdout.write('\nFalse!!!', ending='') #need to modify


