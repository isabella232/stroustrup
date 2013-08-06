from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from models import Book

class BookListView(ListView):

    model = Book

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        return context

class AddBookView(FormView):
    """
    A version of FormView which passes extra arguments to certain
    methods, notably passing the HTTP request nearly everywhere, to
    enable finer-grained processing.

    """
    def get(self, request, *args, **kwargs):
        # Pass request to get_form_class and get_form for per-request
        # form control.
        form_class = self.get_form_class(request)
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        # Pass request to get_form_class and get_form for per-request
        # form control.
        form_class = self.get_form_class(request)
        form = self.get_form(form_class)
        if form.is_valid():
            # Pass request to form_valid.
            return self.form_valid(request, form)
        else:
            return self.form_invalid(form)

    def get_form_class(self, request=None):
        return super(AddBookView, self).get_form_class()

    def get_form_kwargs(self, request=None, form_class=None):
        return super(AddBookView, self).get_form_kwargs()

    def get_initial(self, request=None):
        return super(AddBookView, self).get_initial()

    def get_success_url(self, request=None, user=None):
        # We need to be able to use the request and the new user when
        # constructing success_url.
        return super(AddBookView, self).get_success_url()

    def form_valid(self, form, request=None):
        return super(AddBookView, self).form_valid(form)

    def form_invalid(self, form, request=None):
        return super(AddBookView, self).form_invalid(form)



def main_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('profile:profile'))
    else:
        template = loader.get_template('main/mainpage.html')
        context = RequestContext(request,)
        return HttpResponse(template.render(context))
