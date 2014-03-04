from django.db import models


class FileStorage(models.Model):
    file_name = models.CharField(max_length=100)
    blob = models.BinaryField()
    content_type = models.CharField(max_length=100)
    size = models.BigIntegerField()