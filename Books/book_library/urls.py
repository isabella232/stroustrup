from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django import forms
from models import Book, Book_Tag, Author
from forms import BookForm, Book_TagForm, AuthorForm, ChangeBookForm, SureForm, SearchForm
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic import DetailView
import book_urls

import views

urlpatterns = patterns('',
                       url(r'^$', views.BookListView.as_view(queryset=Book.books.all(),
                                                   context_object_name='books_list',
                                                   template_name='book_library/book_list.html'
                                                   ),
                           name='list'),
                       url(r'^(?P<pk>\d+)/', include(book_urls, namespace='book')),
                       url(r'^busy/$', views.BookListView.as_view(queryset=Book.books.filter(busy=True),
                                                       context_object_name='books_list',
                                                       template_name='book_library/book_list.html'),
                           name='busy'),
                       url(r'^not_busy/$', views.BookListView.as_view(queryset=Book.books.filter(busy=False),
                                                       context_object_name='books_list',
                                                       template_name='book_library/book_list.html'),
                           name='not_busy'),
                       url(r'^not_busy/$', views.BookListView.as_view(queryset=Book.books.filter(busy=False),
                                                       context_object_name='books_list',
                                                       template_name='book_library/book_list.html'),
                           name='not_busy'),
                       url(r'search_results/$', views.SearchResultsView.as_view(template_name="book_library/book_list.html",
                                                                                context_object_name='books_list'),
                           name='search_results'),
                       url(r'add/$', views.AddBookView.as_view(form_class=BookForm,
                                                       success_url="/",
                                                       template_name="book_library/add_book.html"
                                                       ),
                           name='add'),
                       url(r'book_added/$', TemplateView.as_view(
                           template_name="book_library/book_added.html"
                                                   ),
                           ),
                       url(r'add_tag/$', views.AddTagView.as_view(form_class=Book_TagForm,
                                                       success_url="/",
                                                       template_name="book_library/add_tag.html"
                                                       ),
                           name='add_tag'),
                       url(r'add_author/$', views.AddAuthorView.as_view(form_class=AuthorForm,
                                                       success_url="/",
                                                       template_name="book_library/add_author.html"
                                                       ),
                           name='add_author'),
                       url(r'^(?P<pk>\d+)/$', views.ShowBookView.as_view(model=Book,
                                                       template_name="book_library/book.html"
                                                       ),
                           name='book'),
                       url(r'^authors/(?P<pk>\d+)/$', DetailView.as_view(model=Author,
                                                       template_name="book_library/author.html"
                                                       ),
                           name='author'),

                       url(r'^tags/(?P<pk>\w[\w|\s]+\w)/', DetailView.as_view(model=Book_Tag,
                                                       template_name="book_library/tag.html"
                                                       ),
                           name='tag'),
                       )