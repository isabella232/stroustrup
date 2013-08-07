from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.template.response import TemplateResponse
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
import settings, forms, models
from django.shortcuts import render_to_response


class BookView(FormView):

    def get(self,request, *args, **kwargs):
        if request.user.is_active:
            return super(BookView, self).get(request, *args, **kwargs)
        else:
            return render_to_response("main/you_are_not_user.html")


class AddBookView(BookView):

    def post(self, request, *args, **kwargs):
        form = forms.BookForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.files['picture']
            book = models.Book.books.create_new_book(form.cleaned_data)
            book.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class AddAuthorView(BookView):

    def post(self, request, *args, **kwargs):
        form = forms.AuthorForm(request.POST)
        if form.is_valid():
            author = forms.Author.objects.create_new_author(form.cleaned_data)
            author.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ShowBookView(DetailView):
    model = models.Book

    def get_context_data(self, **kwargs):
        context = super(ShowBookView, self).get_context_data(**kwargs)
        context['media'] = settings.MEDIA_ROOT
        context['static'] = settings.STATIC_URL
        return context


class AddTagView(BookView):

    def post(self, request, *args, **kwargs):
        form = forms.Book_TagForm(request.POST)
        if form.is_valid():
            tag = models.Book_Tag.tags.create_new_tag(form.cleaned_data)
            tag.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ChangeBookView(BookView):

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            form = super(BookView, self).get_form_class()
            return super(BookView, self).render_to_response(super(BookView,
                                                                  self).get_context_data(form=form, pk=kwargs['pk']))
        else:
            return render_to_response("main/you_are_not_staff.html")

    def post(self, request, *args, **kwargs):
        form = forms.ChangeBookForm(request.POST)
        if form.is_valid():
            book = models.Book.books.filter(pk=kwargs['pk'])[0]
            book.change(form.cleaned_data)
            book.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class DeleteBookView(ChangeBookView):

    def post(self, request, *args, **kwargs):
        form = forms.SureForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['confirm']:
                book = models.Book.books.filter(pk=kwargs['pk'])[0]
                book.delete()
        return self.form_valid(form)


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


def ReturnBookView(request, **kwargs):
    book = models.Book.books.get(id=kwargs['pk'])
    try:
            client = request.user.library_client
    except:
        client = models.Library_Client()
        if request.user:
            client.user = User.objects.get(username=request.user.username)
            return render_to_response("book_library/you_have_no_book.html")
        else:
            render_to_response("main/you_are_not_user.html")
    if book.busy and client.books.filter(id=book.id):
        book.return_by(client)
        client.save()
        request.user.save()
        book.save()
    return HttpResponseRedirect("..")


class BookListView(ListView):

    model = models.Book

    def get_context_data(self, *args, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        return context


class BookStoryView(TemplateView):

    def get(self, *args, **kwargs):
        record_list = models.Client_Story_Record.objects.filter(book__id=kwargs['pk'])
        return self.render_to_response({'records_list': record_list, 'book_id': record_list[0].book.id})


class SearchResultsView(ListView):

    model = models.Book

    def get_context_data(self, *args, **kwargs):

        context = super(SearchResultsView, self).get_context_data( **kwargs)
        context = {'search_flag': True}
        return context

    def post(self, request, *args):
        form = forms.SearchForm(request.POST)
        books = models.Book.books.filter(isbn=0)
        if form.is_valid():
            if form.cleaned_data['keywords']:
                keywords = form['keywords']
                keywords = list(set(keywords.data.split(' ')))  #deleting equals
                for keyword in keywords:
                    filtered = models.Book.books.filter(title__icontains=keyword)
                    filtered = filtered | models.Book.books.filter(isbn__icontains=keyword)
                    filtered = filtered | models.Book.books.filter(description__icontains=keyword)
                    for author in models.Author.objects.filter(first_name__icontains=keyword):
                        for book in author.books:
                            filtered = filtered | author.books.all()
                    for author in models.Author.objects.filter(last_name__icontains=keyword):
                            filtered = filtered | author.books.all()
                    for author in models.Author.objects.filter(middle_name__icontains=keyword):
                        for book in author.books:
                            filtered = filtered | author.books.all()
                    books = books | filtered
                books.order_by("title")
            return TemplateResponse(request, 'book_library/book_list.html', {'books_list': books,'search_flag': True})


