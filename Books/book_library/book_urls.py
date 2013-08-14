from django.conf.urls import patterns
from django.conf.urls import url
from models import Book
import views

urlpatterns = patterns('',
                       url(r'^$', views.BookView.as_view(template_name="book_library/book.html",
                                                         ),
                           name='book'),
                       url(r'^change/$', views.BookUpdate.as_view(success_url="/",
                                                                  template_name="book_library/change_book.html",
                                                                  ),
                           name='change'),
                       url(r'^delete/$', views.DeleteBook.as_view(success_url="/",
                                                                  ),
                           name='delete'),
                       url(r'^take/$', views.take_book_view, name='take'),
                       url(r'^return/$', views.return_book_view, name='return'),
                       url(r'^story/$', views.BookStoryListView.as_view(template_name='book_library/book_story.html',
                                                                    ),
                           name='story'),
                       url(r'^ask_to_return/$', views.ask_to_return,
                           name='ask'),
                       )