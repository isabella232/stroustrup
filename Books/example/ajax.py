from django.utils import simplejson


def sayhello(request):
    return simplejson.dumps({'message':'Hello World'})