from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from models import Book
from django import forms

from views import BookListView, AddBookView

urlpatterns = patterns('',
                       url(r'^$', BookListView.as_view(queryset=,
                                                       context_object_name='books_list'),
                           name='list'),
                       url(r'^$', AddBookView.as_view(form_class=forms.Form(Book),
                                                       success_url="mainpage",
                                                       ),
                           name='add'),
                       )
