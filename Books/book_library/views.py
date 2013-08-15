from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
import forms, models
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic import DetailView
from profile.views import get_users_books
from django.core.urlresolvers import reverse
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from django.core import mail
from django.contrib.sites.models import RequestSite
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.db.models import Q

@dajaxice_register
def example(request):
    return simplejson.dumps({'message': 'Hello from Python!'})


class BookFormView(FormView):
    form_class = forms.BookForm

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def get(self, request, *args, **kwargs):
        return super(BookFormView, self).get(self, request, *args, **kwargs)


class BookView(DetailView):
    model = models.Book

    def get_context_data(self, **kwargs):
        context = super(BookView, self).get_context_data()
        if context['book'].busy:
            context['book_user'] = context['book'].client_story_record_set.latest('book_taken').user
        return context


class AddView(CreateView):

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def get(self, request, *args, **kwargs):
        return super(AddView, self).get(self, request, *args, **kwargs)


class AuthorAdd(AddView):
    model = models.Author
    form_class = forms.AuthorForm


class TagAdd(AddView):
    model = models.Book_Tag
    form_class = forms.Book_TagForm


class BookAdd(AddView):
    model = models.Book
    form_class = forms.BookForm
    object = None


class BookUpdate(UpdateView):
    model = models.Book
    form_class = forms.BookForm

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def get(self, request, *args, **kwargs):
        return super(BookUpdate, self).get(self, request, *args, **kwargs)


class Delete(DeleteView):

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def get(self, request, *args, **kwargs):
        return super(Delete, self).get(self, request, *args, **kwargs)


class DeleteBook(Delete):
    model = models.Book


class DeleteTag(Delete):
    model = models.Book_Tag


class DeleteAuthor(Delete):
    model = models.Author

@dajaxice_register()
@login_required
def take_book_view(request, **kwargs):
    book = models.Book.books.get(id=kwargs['pk'])
    if not book.busy:
        client = request.user
        book.take_by(client)
        book.save()
        if request.is_ajax():
            return simplejson.dumps({'message': 'Book taken'})
    return HttpResponseRedirect(reverse('mainpage'))

@dajaxice_register
@login_required
def return_book_view(request, **kwargs):
    book = models.Book.books.get(id=kwargs['pk'])
    client = request.user
    books = get_users_books(client)
    if book.busy and books and book in books:
        book.return_by(client)
        book.save()
        if request.is_ajax():
            return simplejson.dumps({'message': 'Book returned'})
    return HttpResponseRedirect(reverse('mainpage'))


class BookListView(FormView):
    busy = None
    form_class = forms.SearchForm
    object_list = None

    @method_decorator(login_required())
    def get(self, request, *args, **kwargs):
        if request.GET:
            form = forms.SearchForm(request.GET)
            filtered = models.Book.books.all()
            if form.is_valid():
                query = Q()
                if form.cleaned_data['keywords']:
                    keywords = form['keywords']
                    keywords = list(set(keywords.data.split(' ')))  #deleting equals
                    for keyword in keywords:
                        query = Q(isbn__iexact=keyword)
                        if not models.Book.books.filter(query):
                            query = Q(description__icontains=keyword) | Q(title__icontains=keyword)
                            query = query | Q(authors__first_name__iexact=keyword) | Q(authors__last_name__iexact=keyword)
                            query = query | Q(tags__tag__iexact=keyword)
                if query:
                    filtered = models.Book.books.filter(query).order_by("title")
                    filtered = set(filtered)  #deleting equals
                else:
                    filtered = models.Book.books.all()
                self.busy = form.cleaned_data['busy']
                if not self.busy is None:
                    if self.busy:
                        filtered = filtered.filter(busy=True)
                    else:
                        filtered = filtered.filter(busy=False)
                return self.render_to_response({'books_list': filtered, 'form': forms.SearchForm})
        else:
            return super(BookListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {'books_list': models.Book.books.all(), "form" : self.get_form(self.form_class)}
        return super(BookListView, self).get_context_data(**context)


class BookStoryListView(ListView):

    @method_decorator(login_required())
    def get(self, request, *args, **kwargs):
        return super(BookStoryListView, self).get(request, *args, **kwargs)

    model = models.Client_Story_Record

    def get_context_data(self, **kwargs):
        context = {}
        pk = self.kwargs['pk']
        records_list = models.Client_Story_Record.records.filter(book__id=pk)
        context['object_list'] = records_list
        context['pk'] = pk
        return super(BookStoryListView, self).get_context_data(**context)

def ask_to_return(request, **kwargs):
    book = get_object_or_404(models.Book, pk=kwargs['pk'])
    if book.busy:
        profile = book.taken_by()
        if request.user != profile:
            authors_string = ""
            for author in book.authors.all():
                authors_string += author.__unicode__()
            site = RequestSite(request)
            server_email = "testemail@" + site.domain
            email = mail.EmailMessage('Book return request', "User %(username)s (%(firstname)s %(lastname)s) asks you"
                                                             " to return the book %(book)s %(author)s."
                                                             " You can return it by click on this link: %(link)s"%
                                                             {'username': request.user.username,
                                                              'firstname': request.user.first_name,
                                                              'lastname': request.user.last_name,
                                                              'book': book.__unicode__(),
                                                              'author': authors_string,
                                                              'link': "http:/%(site)s/books/%(id)s/return/"
                                                                      % {'id': book.id, 'site': site.domain}
                                                             },
                                      server_email,
                                      [profile.email])
            email.send()
            return render_to_response('asked_successfully.html', {'book': book})
    return HttpResponseRedirect("..")