from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
import forms, models
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test


class BookFormView(FormView):
    form_class = forms.BookForm

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def get(self, request, *args, **kwargs):
        return super(BookFormView, self).get(self, request, *args, **kwargs)


class AddView(BookFormView):

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ChangeBookView(BookFormView):

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def get(self, request, *args, **kwargs):
            form = self.get_form_class()
            book = models.Book.books.get(pk=kwargs['pk'])
            form = form(instance=book)
            return self.render_to_response(super(BookFormView, self).get_context_data(form=form, pk=kwargs['pk']))

    def post(self, request, *args, **kwargs):
        book = models.Book.books.get(pk=kwargs['pk'])
        form = forms.BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            if not form.cleaned_data['picture']:
                book.picture = None
            book.save()
            book = form.save()
            return self.form_valid(form)
        return self.form_invalid(form)


class DeleteBookView(BookFormView):

    def post(self, request, *args, **kwargs):
        form = forms.SureForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['confirm']:
                book = models.Book.books.filter(pk=kwargs['pk'])[0]
                book.delete()
        return self.form_valid(form)

@login_required
def TakeBookView(request, **kwargs):
    book = models.Book.books.get(id=kwargs['pk'])
    if not book.busy:
        try:
            client = request.user.library_client
        except:
            client = models.Library_Client()
            client.user = User.objects.get(username=request.user.username)
        book.take_by(client)
        client.save()
        request.user.save()
        book.save()
    return HttpResponseRedirect("..")

@login_required
def ReturnBookView(request, **kwargs):
    book = models.Book.books.get(id=kwargs['pk'])
    try:
        client = request.user.library_client
    except:
        client = models.Library_Client()
        client.user = User.objects.get(username=request.user.username)
        return render_to_response("book_library/you_have_no_book.html")
    if book.busy and client.books.filter(id=book.id):
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