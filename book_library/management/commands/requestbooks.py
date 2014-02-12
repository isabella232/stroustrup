__author__ = 'romanusynin'
from book_library.models import Request_Return
from django.core.management.base import NoArgsCommand
from django.core.urlresolvers import reverse
from django.conf import settings
from datetime import datetime
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from urlparse import urljoin


class Command(NoArgsCommand):

        def handle(self, *args, **options):
            query = Request_Return.objects.order_by("book__id", "id").distinct('book')
            for request_return in query:
                    book = request_return.book
                    authors = u", ".join(unicode(v) for v in book.authors.all())
                    round_day = datetime
                    server_email = settings.EMAIL_HOST_USER
                    link = urljoin('http://{}'.format(Site.objects.get_current().domain), reverse('books:book', kwargs={'pk': book.id}))
                    context = {'book': book, 'authors': authors, 'link': link}
                    if book.busy is False:
                        user = request_return.user_request
                        msg = render_to_string('book_free_email.txt', context)
                        send_mail('Book free', msg, 'Stroustrup Library', [user.email])
                        request_return.delete()
                        continue
                    if request_return.processing_time is not None:
                        round_day = datetime.now() - request_return.processing_time
                    if book.taken_about() == settings.DEADLINE and (request_return.processing_time is None or round_day.days > 0):
                        user = book.taken_by()
                        msg = render_to_string('book_return_request_mail.txt', context)
                        send_mail('Book has been returned', msg, 'Stroustrup Library', [user.email])
                        request_return.processing_time = datetime.now()
                        request_return.save()
