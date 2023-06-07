from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    name = models.CharField(max_length=48, blank=False, null=False)
    description = models.TextField()
    date_until = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)