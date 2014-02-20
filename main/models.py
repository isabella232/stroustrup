from django.db import models


class FileStorage(models.Model):
    file_name = models.CharField(max_length=100)
    blob = models.BinaryField()
    size = models.BigIntegerField()