from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
import forms, models
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic import DetailView
from profile.views import get_users_books


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


@login_required
def take_book_view(request, **kwargs):
    book = models.Book.books.get(id=kwargs['pk'])
    if not book.busy:
        client = request.user
        book.take_by(client)
        client.save()
        request.user.save()
        book.save()
    return HttpResponseRedirect("..")

@login_required
def return_book_view(request, **kwargs):
    book = models.Book.books.get(id=kwargs['pk'])
    client = request.user
    books = get_users_books(client)
    if book.busy and books and book in books:
        book.return_by(client)
        client.save()
        request.user.save()
        book.save()
    return HttpResponseRedirect("..")


class BookListView(ListView):
    busy = None
    object_list = None
    queryset = models.Book.books.all()

    @method_decorator(login_required())
    def get(self, request, *args, **kwargs):
        return super(BookListView, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['form'] = forms.SearchForm
        return context

    @method_decorator(login_required())
    def post(self, request, *args):
        form = forms.SearchForm(request.POST)
        filtered = models.Book.books.all()
        if form.is_valid():
            if form.cleaned_data['keywords']:
                keywords = form['keywords']
                keywords = list(set(keywords.data.split(' ')))  #deleting equals
                #base_found = True
                for keyword in keywords:
                    filtered = filtered.filter(title__icontains=keyword)
                    filtered = filtered | models.Book.books.filter(isbn__iexact=keyword)
                    filtered = filtered | models.Book.books.filter(description__icontains=keyword)
                    for author in models.Author.authors.filter(first_name__iexact=keyword):
                        filtered = filtered | author.books.all()
                    for author in models.Author.authors.filter(last_name__iexact=keyword):
                        filtered = filtered | author.books.all()
                    for author in models.Author.authors.filter(middle_name__iexact=keyword):
                        filtered = filtered | author.books.all()
                    for tag in models.Book_Tag.tags.filter(tag__iexact=keyword):
                        filtered = filtered | tag.books.all()
                    # if not base_found:
                    #     books = filtered
                    #     if books:
                    #         base_found = True
                    # else:
                    #     books = filtered
            filtered.order_by("title")
            self.busy = form.cleaned_data['busy']
            if not self.busy is None:
                if self.busy:
                    filtered = filtered.filter(busy=True)
                else:
                    filtered = filtered.filter(busy=False)
            return self.render_to_response({'books_list': filtered, 'form': forms.SearchForm})


class BookStoryListView(ListView):

    @method_decorator(login_required())
    def get(self, request, *args, **kwargs):
        return super(BookStoryListView, self).get(request, *args, **kwargs)

    model = models.Client_Story_Record

    def get_context_data(self, *args, **kwargs):
        context = {}
        pk = self.kwargs['pk']
        records_list = models.Client_Story_Record.records.filter(book__id=pk)
        context['records_list'] = records_list
        context['pk'] = pk
        return context