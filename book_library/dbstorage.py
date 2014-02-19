import psycopg2
from storages.backends.database import DatabaseStorage
from django.conf import settings
import os
from django.http import HttpResponse
from django.utils._os import safe_join
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, IntegrityError
REQUIRED_FIELDS = ('db_table', 'fname_column', 'blob_column', 'size_column', 'base_url')


class DatabaseStoragePostgres(DatabaseStorage):

    def __init__(self, option=settings.DB_FILES):
        if not option or not all([field in option for field in REQUIRED_FIELDS]):
            raise ValueError("You didn't specify required options")

        self.db_table = option['db_table']
        self.fname_column = option['fname_column']
        self.blob_column = option['blob_column']
        self.size_column = option['size_column']
        self.base_url = option['base_url']
        self.connection = psycopg2.connect("host='localhost' port='5433' dbname='postgres' user='postgres' password='admin'")
        self.cursor = self.connection.cursor()

    def exists(self, name):
        row = self.cursor.execute("SELECT %s from %s where %s = '%s'"%(self.fname_column,
                                                                       self.db_table,
                                                                       self.fname_column,
                                                                       name))
        if row is not None:
            return row.fetchone()

    def _save(self, name, content):
        """Save 'content' as file named 'name'.

        @note '\' in path will be converted to '/'.
        """

        name = name.replace('\\', '/')
        binary = psycopg2.Binary(content.read())
        size = content.size

        #todo: check result and do something (exception?) if failed.
        if self.exists(name):
            self.cursor.execute("UPDATE %s SET %s = %s, %s = %s WHERE %s = '%s'" % (self.db_table,
                                                                                    self.blob_column,
                                                                                    self.size_column,
                                                                                    self.fname_column,
                                                                                    name, binary, size))
        else:
            # try:
                self.cursor.execute("INSERT INTO %s VALUES('%s',%s,%s)" % (self.db_table, name, binary, size))
            # except IntegrityError:
            #     transaction.rollback()
            # self.cursor.execute("INSERT INTO %s VALUES('%s',%s,%s)" % (self.db_table, name, binary, size))
        self.connection.commit()
        return name


def image_view(request, filename):


    storage = DatabaseStoragePostgres()

    try:
        image_file = storage.open(filename, 'rb')
        file_content = image_file.read()
    except:
        filename = 'no_image.gif'
        path = safe_join(os.path.abspath(settings.MEDIA_ROOT), filename)
        if not os.path.exists(path):
            raise ObjectDoesNotExist
        no_image = open(path, 'rb')
        file_content = no_image.read()

    response = HttpResponse(file_content, mimetype="image/jpeg")
    response['Content-Disposition'] = 'inline; filename=%s'%filename
    return response