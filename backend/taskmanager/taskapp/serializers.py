from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from .models import Task


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "done", "name", "description", "date_until", "user")