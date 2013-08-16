from django.views.generic import DetailView
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView
import forms


class ProfileView(DetailView):
    model = User

    def get_context_data(self, object):
        context = {'profile': object, 'books': object.get_users_books(), 'user': self.request.user}
        return super(ProfileView, self).get_context_data(**context)


class ProfileFormView(UpdateView):
    model = User
    form_class = forms.ProfileForm