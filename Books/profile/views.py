from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext, loader
from forms import ProfileForm


@login_required
def profile(request):
    user = request.user
    template = loader.get_template('profile.html')
    context = RequestContext(request,{'user':user})
    return HttpResponse(template.render(context))

@login_required
def profile_change(request):
    user = request.user
    if request.method == 'POST': # If the form has been submitted...
        form = ProfileForm(request.POST)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return HttpResponseRedirect(reverse('profile:profile', args=()))
    else:
        form=ProfileForm()
        context=RequestContext(request,{'user':user,'form':form})
        return render_to_response('profile_change.html',
                       context, context_instance=RequestContext(request))