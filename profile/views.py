from django.views.generic import DetailView, ListView
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.template.response import TemplateResponse
from book_library.views import LoginRequiredView
import forms


class ProfileView(LoginRequiredView, DetailView):
    model = User

    def get_context_data(self, object):
        context = {'profile': object, 'books': object.get_users_books()}
        return super(ProfileView, self).get_context_data(**context)


@csrf_protect
@login_required
def profile_change(request):
    template_name = 'profile_change.html'
    profile_change_form = forms.ProfileForm
    post_change_redirect = reverse("profile:profile", args=str(request.user.pk))
    if request.method == "POST":
        form = profile_change_form(user=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(post_change_redirect)
        else:
            context = {'form': form}
            return TemplateResponse(request, template_name, context)
    else:
        form = profile_change_form(user=request.user)
        context = {'form': form}
        return TemplateResponse(request, template_name, context)

class UsersView(LoginRequiredView, ListView):
    model = User
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        return super(UsersView, self).get(request, *args, **kwargs)