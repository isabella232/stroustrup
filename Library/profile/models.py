import datetime
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator
from django.contrib import auth



class Profile_addition(models.Model):
    user=models.ForeignKey(User)
    avatar=models.FileField(upload_to='user_avatar')
