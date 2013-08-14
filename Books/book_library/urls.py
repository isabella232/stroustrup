from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from models import Author, Book_Tag
from django.views.generic import DetailView
import book_urls

import views

urlpatterns = patterns('',
<<<<<<< HEAD
                       url(r'^$', views.BookListView.as_view(template_name='book_library/book_list.html',
=======
                       url(r'^$', views.BookListView.as_view(context_object_name='books_list',
                                                             template_name='book_library/book_list.html',
>>>>>>> 9c0a6af58166aef9d53fcd202e26d0c5d585cb20
                                                             ),
                           name='list'),
                       url(r'^(?P<pk>\d+)/', include(book_urls, namespace='book')),
                       url(r'add/$', views.BookAdd.as_view(success_url="/",
                                                           template_name="book_library/add_book.html",
                                                           ),
                           name='add'),
                       url(r'add_tag/$', views.TagAdd.as_view(success_url="/",
                                                              template_name="book_library/add_author_or_tag.html",
                                                              ),
                           name='add_tag'),
                       url(r'add_author/$', views.AuthorAdd.as_view(success_url="/",
                                                                    template_name="book_library/add_author_or_tag.html",
                                                                    ),
                           name='add_author'),
                       url(r'^authors/(?P<pk>\d+)/$', DetailView.as_view(model=Author,
                                                                         template_name="book_library/author.html",
                                                                         ),
                           name='author'),

                       url(r'^tags/(?P<pk>\d+)/$', DetailView.as_view(model=Book_Tag,
                                                                      template_name="book_library/tag.html",
                                                                      ),
                           name='tag'),
                       )