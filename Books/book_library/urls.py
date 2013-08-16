from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from models import Author, Book_Tag, Book_Request
from django.views.generic import DetailView, DeleteView
import book_urls

import views

urlpatterns = patterns('',
                       url(r'^$', views.BookListView.as_view(template_name='book_library/book_list.html',
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
                        url(r'^request/$', views.requestBook.as_view(    success_url='/',
                            model=Book_Request,
                            template_name='book_library/request_new.html'
                                                                    ),
                        name='request'),
                        #SpaT edition
                       )