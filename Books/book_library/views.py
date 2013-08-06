from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.template.response import TemplateResponse
from django.views.generic.edit import FormView
from django.db.models.query import QuerySet

from models import Book, Book_Tag, Author
from forms import BookForm, Book_TagForm, AuthorForm, ChangeBookForm, SureForm, SearchForm
from django.shortcuts import render_to_response


class BookView(FormView):

    def get(self,request):
        if request.user.is_staff:
            return super(BookView, self).get(request)
        else:
            return render_to_response("book_library/you_are_not_staff.html")


class AddBookView(BookView):

    def post(self, request, *args, **kwargs):
        # Pass request to get_form_class and get_form for per-request
        # form control.

        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.files['picture']
            book = Book.books.create_new_book(form.cleaned_data)
            book.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class AddAuthorView(BookView):


    def post(self, request, *args, **kwargs):
        # Pass request to get_form_class and get_form for per-request
        # form control.

        form = AuthorForm(request.POST)
        if form.is_valid():
            author = Author.objects.create_new_author(form.cleaned_data)
            author.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class AddTagView(BookView):

    def post(self, request, *args, **kwargs):
        # Pass request to get_form_class and get_form for per-request
        # form control.

        form = Book_TagForm(request.POST)
        if form.is_valid():
            tag = Book_Tag.tags.create_new_tag(form.cleaned_data)
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
            return render_to_response("book_library/you_are_not_staff.html")

    def post(self, request, *args, **kwargs):
        # Pass request to get_form_class and get_form for per-request
        # form control.

        form = ChangeBookForm(request.POST)
        if form.is_valid():
            book = Book.books.filter(pk=kwargs['pk'])[0]
            book.change(form.cleaned_data)
            book.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class DeleteBookView(ChangeBookView):

    def post(self, request, *args, **kwargs):
        # Pass request to get_form_class and get_form for per-request
        # form control.
        form = SureForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['confirm']:
                book = Book.books.filter(pk=kwargs['pk'])[0]
                book.delete()
        return self.form_valid(form)


class BookListView(ListView):

    model = Book

    def get_context_data(self, *args, **kwargs):
        context = super(BookListView, self).get_context_data( **kwargs)
        context['form'] = SearchForm()
        return context


class SearchResultsView(ListView):

    model = Book

    def get_context_data(self, *args, **kwargs):

        context = super(SearchResultsView, self).get_context_data( **kwargs)
        context = {'search_flag': True}
        return context

    def post(self, request, *args):
        form = SearchForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['keywords']:
                keywords = form['keywords']
                keywords = list(set(keywords.data.split(' ')))  #deleting equals
                books = Book.books.filter(isbn=0)
                for keyword in keywords:
                    filtered = Book.books.filter(title__icontains=keyword)
                    filtered = filtered | Book.books.filter(isbn__icontains=keyword)
                    filtered = filtered | Book.books.filter(description__icontains=keyword)
                    for author in Author.objects.filter(first_name__icontains=keyword):
                        for book in author.books:
                            filtered = filtered | author.books.all()
                    for author in Author.objects.filter(last_name__icontains=keyword):
                            filtered = filtered | author.books.all()
                    for author in Author.objects.filter(middle_name__icontains=keyword):
                        for book in author.books:
                            filtered = filtered | author.books.all()
                    books = books | filtered
                books.order_by("title")
            return TemplateResponse(request, 'book_library/book_list.html', {'books_list': books,'search_flag': True})
        return self.form_invalid(form)


