from django.contrib.auth import logout
from django.shortcuts import redirect
from Books.views import main_view

def logout_view(request):
    logout(request)
    return redirect(main_view)


