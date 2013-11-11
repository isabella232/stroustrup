from django.conf.urls import patterns, include, url
from models import Author, Book_Tag
from models import Author, Book_Tag, Book_Request
from django.views.generic import DetailView, DeleteView

from views import *

urlpatterns = patterns('',
                       url(r'^(page((?P<page>\d+))/)?((?P<slug>(free|busy))/)?$', BookListView.as_view(template_name='book_library/book_list.html',),
                           name='list'),
                       url(r'add/$', BookAdd.as_view(success_url="/",
                                                           template_name="book_library/add_book.html",
                                                           ),
                           name='add'),
                       url(r'^add_tag/$', TagAdd.as_view(success_url="/",
                                                              template_name="book_library/add_author_or_tag.html",
                                                              ),
                           name='add_tag'),
                       url(r'^add_author/$', AuthorAdd.as_view(success_url="/",
                                                                    template_name="book_library/add_author_or_tag.html",
                                                                    ),
                           name='add_author'),
                       url(r'^authors/(?P<pk>\d+)/$', AuthorView.as_view(model=Author,
                                                                         template_name="book_library/author.html",
                                                                         ),
                           name='author'),
                       url(r'^tags/(?P<pk>\d+)/$', TagView.as_view(model=Book_Tag,
                                                                      template_name="book_library/tag.html",
                                                                      ),
                           name='tag'),
                       url(r'^(?P<pk>\d+)/$', BookView.as_view(template_name="book_library/book.html",
                                                         ),
                           name='book'),
                       url(r'^(?P<pk>\d+)/change/$', BookUpdate.as_view(success_url="/",
                                                                  template_name="book_library/change_book.html",
                                                                  ),
                           name='change'),
                       url(r'^(?P<pk>\d+)/delete/$', DeleteBook.as_view(success_url="/",
                                                                  ),
                           name='delete'),
                       url(r'/take/(\d+)', take_book_view, name='take'),
                       url(r'/return/(\d+)', return_book_view, name='return'),
                       url(r'^(?P<pk>\d+)/story/$', BookStoryListView.as_view(template_name='book_library/book_story.html',
                                                                    ),
                           name='story'),
                       url(r'^(?P<pk>\d+)/ask_to_return/(\d+)$', ask_to_return,
                           name='ask'),
                       #SpaT_edition v
                       url(r'^request/$', requestBook.as_view(success_url='//',
                           model=Book_Request,
                           template_name='book_library/request_new.html'
                       ), name='request'
                       ),
                       url(r'like/(\d+)/$', LikeRequest,
                           name='like'),
                       url(r'^users/$', UsersView.as_view(template_name='book_library/users_list.html'),
                           name = 'users'
                       ),
                       url(r'comment/(\d+)/(.*)$', CommentAdd, name='comment'),
                        url(r'rating/(\d+)', rating_post, name='rating'),
                       #SpaT edition ^
                       )