__author__ = 'romanusynin'
from Library.book_library.models import Request_Return
from django.core.management.base import NoArgsCommand
from Library.main.settings import DOMAIN, DEADLINE, EMAIL_HOST_USER
from datetime import datetime
from django.core.mail import EmailMessage


class Command(NoArgsCommand):


        def handle(self, *args, **options):
            query = Request_Return.objects.order_by("book__id", "id").distinct('book')
            for request_return in query:
                    book = request_return.book
                    authors = u", ".join(unicode(v) for v in book.authors.all())
                    round_day = datetime
                    server_email = EMAIL_HOST_USER
                    if book.busy is False:
                        user = request_return.user_request
                        email = EmailMessage('Book free request',
                                             "Book (''{0}'' author(s): {1}) has been returned."
                                             " You can take it by click on this link: {2}/books/{3}".format(book.title, authors, DOMAIN, book.id),
                                             server_email, [user.email])
                        email.send()
                        request_return.delete()
                        continue
                    if request_return.processing_time is not None:
                        round_day = datetime.now() - request_return.processing_time
                    if book.taken_about() == 0 and (request_return.processing_time is None or round_day.days > 0):
                        user = book.taken_by()
                        email = EmailMessage('Book return request',
                                             "We is asking you to return the book: ''{0}''author(s): {1}"
                                             " You can return it by click on this link: {2}/books/{3}"
                                             .format(book.title, authors, DOMAIN, book.id),
                                             server_email, [user.email])
                        email.send()
                        request_return.processing_time = datetime.now()
                        request_return.save()


