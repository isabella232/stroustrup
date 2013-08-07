from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from forms import ProfileForm


def profile(request):
    if request.user.is_active:
        user = request.user
        template = loader.get_template('profile.html')
        context = RequestContext(request,{'user': user})
        return render_to_response('profile.html', context)
    else:
        return render_to_response('main/you_are_not_user.html')


def profile_change(request):
    if request.user.is_active:
        user = request.user
        if request.method == 'POST':
            form = ProfileForm(request.POST)
            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                context = {'user': user}
                return render_to_response('profile.html', context)
        else:
            form=ProfileForm()
            context=RequestContext(request,{'user':user,'form':form})
            return render_to_response('profile_change.html',
                                      context, context_instance=RequestContext(request))
    else:
        return render_to_response('main/you_are_not_user.html')