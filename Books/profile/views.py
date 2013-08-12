from django.views.generic import DetailView
from django.contrib.auth.models import User
from django.core import mail
from book_library.models import Book
from django.contrib.sites.models import RequestSite
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.views.generic.edit import UpdateView
from django.http import HttpResponseRedirect
import forms


def get_users_books(user):
        books = set()
        for book in Book.books.all():
            if book.taken_by() == user:
                books.add(book.pk)
        if books:
            return Book.books.filter(pk__in=books)
        else:
            return None


class ProfileView(DetailView):
    model = User

    def get_context_data(self, object):
        context = {'profile': object, 'books': get_users_books(object), 'user': self.request.user}
        return super(ProfileView, self).get_context_data(**context)


def ask_to_return(request, *args, **kwargs):
    book = get_object_or_404(Book, pk=kwargs['num'])
    if book.busy:
        profile = get_object_or_404(User, pk=kwargs['pk'])
        authors_string = ""
        for author in book.authors.all():
            authors_string += author.__unicode__()
        site = RequestSite(request)
        email = mail.EmailMessage('Book return request', "User %(username)s (%(firstname)s %(lastname)s) asks you"
                                                         " to return the book %(book)s %(author)s."
                                                         " You can return it by click on this link: %(link)s"%
                                                         {'username': request.user.username,
                                                          'firstname': request.user.first_name,
                                                          'lastname': request.user.last_name,
                                                          'book': book.__unicode__(),
                                                          'author': authors_string,
                                                          'link': "http:/%(site)s/books/%(id)s/return/"
                                                                  %{'id': book.id, 'site': site.domain}
                                                         },
                                  'from@example.com',
                                  [profile.email])
        email.send()
        return render_to_response('asked_successfully.html', {'book': book})
    return HttpResponseRedirect("..")


class ProfileFormView(UpdateView):
    model = User
    form_class = forms.ProfileForm