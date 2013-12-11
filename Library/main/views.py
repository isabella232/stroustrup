from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib import auth

def main_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('books:list'))
    else:
        #template = loader.get_template('main/mainpage.html')
        #context = RequestContext(request,)
        #return HttpResponse(template.render(context))
        return HttpResponseRedirect('/landing_page')

