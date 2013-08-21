from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from models import Author, Book_Tag, Book_Request
from django.views.generic import DetailView, DeleteView
import book_urls

import views

urlpatterns = patterns('',
                       url(r'^((?P<slug>(free|busy))/)?$', views.BookListView.as_view(template_name='book_library/book_list.html',),
                           name='list'),
                       url(r'add/$', views.BookAdd.as_view(success_url="/",
                                                           template_name="book_library/add_book.html",
                                                           ),
                           name='add'),
                       url(r'^add_tag/$', views.TagAdd.as_view(success_url="/",
                                                              template_name="book_library/add_author_or_tag.html",
                                                              ),
                           name='add_tag'),
                       url(r'^add_author/$', views.AuthorAdd.as_view(success_url="/",
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
                       url(r'^(?P<pk>\d+)/$', views.BookView.as_view(template_name="book_library/book.html",
                                                         ),
                           name='book'),
                       url(r'^(?P<pk>\d+)/change/$', views.BookUpdate.as_view(success_url="/",
                                                                  template_name="book_library/change_book.html",
                                                                  ),
                           name='change'),
                       url(r'^(?P<pk>\d+)/delete/$', views.DeleteBook.as_view(success_url="/",
                                                                  ),
                           name='delete'),
                       url(r'^(?P<pk>\d+)/take/$', views.take_book_view, name='take'),
                       url(r'^(?P<pk>\d+)/return/$', views.return_book_view, name='return'),
                       url(r'^(?P<pk>\d+)/story/$', views.BookStoryListView.as_view(template_name='book_library/book_story.html',
                                                                    ),
                           name='story'),
                       url(r'^(?P<pk>\d+)/ask_to_return/$', views.ask_to_return,
                           name='ask'),

                       #SpaT_edition v
                       url(r'^request/', views.requestBook.as_view(success_url='//',
                           model=Book_Request,
                           template_name='book_library/request_new.html'
                       ), name='request'
                       ),
                       url(r'^like/(\d+)/$', views.LikeRequest,
                            name='like'),
                       url(r'^users/', views.UsersView.as_view(template_name='book_library/users_list.html'),
                       name = 'users'
                       ),
                       #SpaT edition ^
                       )