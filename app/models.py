from django.db import models


# Create your models here.

class Information(models.Model):
    headers = models.CharField(max_length=1000000, blank=True)
    ip = models.CharField(max_length=1000, default='127.0.0.1')
    username = models.CharField(max_length=1000, blank=True)
    password = models.CharField(max_length=1000, blank=True)
    country = models.CharField(max_length=1000, blank=True)
    user_agent = models.TextField(blank=True)
    current_date = models.DateField()


class Sqlinjection(models.Model):
    ip = models.CharField(max_length=100)
    usernameInject = models.CharField(max_length=100, blank=True)
    passwordInject = models.CharField(max_length=100, blank=True)
    current_date = models.DateField()
