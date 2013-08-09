from forms import ProfileForm, AskReturnForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.core import mail
from book_library.models import Book
from django.contrib.sites.models import RequestSite
import datetime


def get_users_books(user):
        books = set()
        for book in Book.books.all():
            if book.taken_by() == user:
                books.add(book.pk)
        if books:
            return Book.books.filter(pk__in=books)
        else:
            return None


class ProfileView(FormView):
    form_class = AskReturnForm

    def get_form(self, request):
        profile = User.objects.get(pk=self.kwargs['pk'])
        queryset = get_users_books(profile)
        if queryset:
            return self.form_class(queryset=get_users_books(profile))
        else:
            return None

    def get_context_data(self, form):
        profile = User.objects.get(pk=self.kwargs['pk'])
        context = {'profile': profile, 'books': get_users_books(profile), 'user': self.request.user, 'form': form}
        return super(ProfileView, self).get_context_data(**context)

    def post(self, request, *args, **kwargs):
        profile = User.objects.get(pk=self.kwargs['pk'])
        books = get_users_books(profile)
        form = AskReturnForm(books, request.POST)
        if form.is_valid():
            book = form.cleaned_data['choices']
            authors_string = ""
            for author in book.authors.all():
                authors_string += author.__unicode__()
            connection = mail.get_connection()
            connection.open()
            site = RequestSite(request)
            email = mail.EmailMessage('Book return request', "User %(username)s asks you to return the book %(book)s %(author)s. You can return"\
            "it by click on this link: %(link)s"%{'username': request.user.username, 'book': book.__unicode__(), 'author': authors_string, 'link': "http:/%(site)s/books/%(id)s/return/" % {'id': book.id, 'site': site.domain}}, 'from@example.com',
                                      [profile.email], connection=connection)
            email.send()
            connection.close()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ProfileFormView(FormView):
    form_class = ProfileForm

    @method_decorator(login_required)
    def get(self, request, **kwargs):
        return super(ProfileFormView, self).get(self, request, **kwargs)