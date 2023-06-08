from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User


class UserAPI(APIView):
    def post(self, request):
        if not User.objects.filter(username=request.POST["username"]).exists():
            User.objects.create_user(username=request.POST["username"], password=request.POST["password"])
        return Response({"True"})