from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django import forms
from models import Book, Book_Tag, Author
from forms import BookForm, Book_TagForm, AuthorForm, SureForm, SearchForm
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic import DetailView
import settings

import views

urlpatterns = patterns('',
                       url(r'^$', DetailView.as_view(model=Book,
                                                             template_name="book_library/book.html",
                                                             ),
                           name='book'),
                       url(r'^change/$', views.ChangeBookView.as_view(success_url="/",
                                                                      template_name="book_library/change_book.html",
                                                                      ),
                           name='change'),
                       url(r'^delete/$', views.DeleteBookView.as_view(form_class=SureForm,
                                                                      success_url="/",
                                                                      template_name="book_library/confirmation.html",
                                                                      ),
                           name='delete'),
                       url(r'^take/$', views.take_book_view, name='take'),
                       url(r'^return/$', views.return_book_view, name='return'),
                       url(r'^story/$', views.BookStoryListView.as_view(template_name='book_library/book_story.html',
                                                                    ),
                           name='story'),
                       )