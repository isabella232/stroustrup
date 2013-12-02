from django.views.generic import DetailView, ListView
from django.contrib.auth.models import User
from Library.book_library.views import LoginRequiredView
from django.views.generic.edit import UpdateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

import forms


class ProfileView(LoginRequiredView, DetailView):
    model = User

    def get_context_data(self, object):
        context = {'profile': object, 'books': object.get_users_books(), 'user': self.request.user,}
        return super(ProfileView, self).get_context_data(**context)


class ProfileFormView(UpdateView):
    model = User
    form_class = forms.ProfileForm

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        if request.user.pk == int(kwargs['pk']):
            return super(ProfileFormView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse("profile:all"))


class UsersView(LoginRequiredView, ListView):
    model = User
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        return super(UsersView, self).get(request, *args, **kwargs)