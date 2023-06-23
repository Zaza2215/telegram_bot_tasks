from django.contrib import admin
from .models import Task


@admin.register(Task)
class AuthorAdmin(admin.ModelAdmin):
    fields = ["done", "name", "description", "date", "user"]
