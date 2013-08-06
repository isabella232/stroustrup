from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django import forms
from models import Book, Book_Tag, Author
from forms import BookForm, Book_TagForm, AuthorForm, ChangeBookForm, SureForm, SearchForm
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic import DetailView
import settings

from views import AddBookView, AddTagView, AddAuthorView, ChangeBookView, DeleteBookView, SearchResultsView, BookListView

urlpatterns = patterns('',
                       url(r'^$', BookListView.as_view(queryset=Book.books.all(),
                                                   context_object_name='books_list',
                                                   ),
                           name='list'),
                       url(r'^busy/$', BookListView.as_view(queryset=Book.books.filter(busy=True),
                                                       context_object_name='books_list'),
                           name='busy'),
                       url(r'^not_busy/$', BookListView.as_view(queryset=Book.books.filter(busy=False),
                                                       context_object_name='books_list'),
                           name='not_busy'),
                       url(r'^not_busy/$', BookListView.as_view(queryset=Book.books.filter(busy=False),
                                                       context_object_name='books_list'),
                           name='not_busy'),
                       url(r'search_results/$', SearchResultsView.as_view(template_name="book_library/book_list.html",
                                                                          context_object_name='books_list'
                                                       ),
                           name='search_results'),
                       url(r'add$', AddBookView.as_view(form_class=BookForm,
                                                       success_url="/",
                                                       template_name="book_library/add_book.html"
                                                       ),
                           name='add'),
                       url(r'book_added$', TemplateView.as_view(
                           template_name="book_library/book_added.html"
                                                   ),
                           ),
                       url(r'add_tag$', AddTagView.as_view(form_class=Book_TagForm,
                                                       success_url="/",
                                                       template_name="book_library/add_tag.html"
                                                       ),
                           name='add_tag'),
                       url(r'add_author$', AddAuthorView.as_view(form_class=AuthorForm,
                                                       success_url="/",
                                                       template_name="book_library/add_author.html"
                                                       ),
                           name='add_author'),
                       url(r'^(?P<pk>\d+)$', DetailView.as_view(model=Book,
                                                       template_name="book_library/book.html"
                                                       ),
                           name='book'),
                       url(r'^authors/(?P<pk>\d+)$', DetailView.as_view(model=Author,
                                                       template_name="book_library/author.html"
                                                       ),
                           name='author'),

                       url(r'^tags/(?P<pk>\w[\w|\s]+\w)', DetailView.as_view(model=Book_Tag,
                                                       template_name="book_library/tag.html"
                                                       ),
                           name='tag'),
                       url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
                       url(r'^(?P<pk>\d+)/change/', ChangeBookView.as_view(form_class=ChangeBookForm,
                                                       success_url="/",
                                                       template_name="book_library/change_book.html"
                                                       ),
                           name='change'),
                       url(r'^(?P<pk>\d+)/delete/', DeleteBookView.as_view(form_class=SureForm,
                                                       success_url="/",
                                                       template_name="book_library/delete_book.html"
                                                       ),
                           name='delete'),
                       )