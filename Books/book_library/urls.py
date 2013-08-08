from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django import forms
from models import Book, Book_Tag, Author
import forms
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic import DetailView
import book_urls
from django.contrib.auth.decorators import login_required

import views

urlpatterns = patterns('',
                       url(r'^$', views.BookListView.as_view(context_object_name='books_list',
                                                             template_name='book_library/book_list.html',
                                                             ),
                           name='list'),
                       url(r'^(?P<pk>\d+)/', include(book_urls, namespace='book')),
                       url(r'add/$', views.AddView.as_view(form_class=forms.BookForm,
                                                           success_url="/",
                                                           template_name="book_library/add_book.html",
                                                           ),
                           name='add'),
                       url(r'book_added/$', TemplateView.as_view(template_name="book_library/book_added.html",
                                                                 ),
                           ),
                       url(r'add_tag/$', views.AddView.as_view(form_class=forms.Book_TagForm,
                                                                  success_url="/",
                                                                  template_name="book_library/add_author_or_tag.html",
                                                                  ),
                           name='add_tag'),
                       url(r'add_author/$', views.AddView.as_view(form_class=forms.AuthorForm,
                                                                        success_url="/",
                                                                        template_name="book_library/add_author_or_tag.html",
                                                                        ),
                           name='add_author'),
                       url(r'^authors/(?P<pk>\d+)/$', DetailView.as_view(model=Author,
                                                                         template_name="book_library/author.html",
                                                                         ),
                           name='author'),

                       url(r'^tags/(?P<pk>\w[\w|\s]+\w)/', DetailView.as_view(model=Book_Tag,
                                                                              template_name="book_library/tag.html",
                                                                              ),
                           name='tag'),
                       )