from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist

from .models import Task
from. serializers import TaskSerializer


class UserAPI(APIView):
    def post(self, request):
        if not User.objects.filter(username=request.POST["username"]).exists():
            User.objects.create_user(username=request.POST["username"], password=request.POST["password"])
        return Response("Success")


class TaskAPI(APIView):
    def get(self, request):
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if not user:
            return Response("The user isn't exist", status=404)

        pk = request.POST.get("id", None)

        if pk:
            task = Task.objects.filter(pk=pk, user=user)
            if task.exists():
                return Response(TaskSerializer(task[0]).data)
            else:
                return Response("The task isn't exist", status=404)
        else:
            tasks = Task.objects.filter(user=user)
            return Response(TaskSerializer(tasks, many=True).data)

    def post(self, request):
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if not user:
            return Response("The user isn't exist")

        task_data = {
            "name": request.POST["name"],
            "description": request.POST["description"],
            "date_until": request.POST.get("date", None),
            "user": user
        }

        task = Task.objects.create(**task_data)
        return Response(TaskSerializer(task).data)

    def put(self, request):
        fields = ["name", "description", "date", "date_until"]
        task_data = {}

        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if not user:
            return Response("The user isn't exist", status=404)


        task = Task.objects.filter(id=request.POST["id"])
        if not task:
            return Response("The task isn't exist", status=404)
        else:
            for key, value in request.POST.items():
                if key in fields:
                    task_data[key] = value

            task.update(**task_data)

        return Response(TaskSerializer(task[0]).data)

    def delete(self, request):
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if not user:
            return Response("The user isn't exist", status=404)

        try:
            task = Task.objects.get(pk=request.POST["id"])
            task.delete()
        except ObjectDoesNotExist:
            return Response("This task")

        return Response(TaskSerializer(task).data)