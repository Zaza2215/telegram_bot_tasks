from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    done = models.BooleanField(default=False)
    name = models.CharField(max_length=48, blank=False, null=False)
    description = models.TextField()
    date = models.DateField(default=None, null=True)
    member = models.IntegerField()
