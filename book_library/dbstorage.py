from django.core.files.storage import Storage
from django.conf import settings
from django.http import HttpResponse, Http404, HttpResponseNotModified
from django.core.exceptions import ObjectDoesNotExist
from main.models import FileStorage
import StringIO
import urlparse
from django.core.files import File
import mimetypes


class DatabaseStoragePostgres(Storage):

    def __init__(self):
        self.base_url = settings.DB_FILES_URL

    def _open(self, name, mode='rb'):
        try:
            media_file = FileStorage.objects.get(file_name=name)
        except ObjectDoesNotExist:
            return None
        return media_file

    def exists(self, name):
        blob = FileStorage.objects.filter(file_name=name)
        return blob

    def _save(self, name, content):
        name = name.replace('\\', '/')
        content_type, encoding = mimetypes.guess_type(name)
        content_type = content_type or 'application/octet-stream'
        binary = content.read()
        size = content.size
        while self.exists(name):
            dot_index = name.rindex('.')
            name = name[:dot_index] + '_1' + name[dot_index:]
        FileStorage.objects.create(file_name=name, blob=binary, content_type=content_type, size=size)
        return name

    def url(self, name):
        if self.base_url is None:
            raise ValueError("This file is not accessible via a URL.")
        return urlparse.urljoin(self.base_url, name).replace('\\', '/')

    def get_available_name(self, name):
        return name

    def delete(self, name):
        FileStorage.objects.filter(file_name=name).delete()


def file_view(request, filename):
    storage = DatabaseStoragePostgres()
    file_object = storage.open(filename, 'rb')
    inMemFile = StringIO.StringIO(file_object.blob)
    inMemFile.name = file_object.file_name
    inMemFile.mode = 'rb'
    ready_file = File(inMemFile)
    content_type = file_object.content_type
    if ready_file is None:
        raise Http404
    else:
        file_content = ready_file.read()
    if request.META.get('HTTP_IF_MODIFIED_SINCE') is not None:
        return HttpResponseNotModified()
    response = HttpResponse(file_content, content_type=content_type)
    response['Content-Disposition'] = 'inline; filename=%s' % filename
    return response