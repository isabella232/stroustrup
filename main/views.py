from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


def main_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('books:list'))
    else:
        return HttpResponseRedirect(reverse('auth_login'))

