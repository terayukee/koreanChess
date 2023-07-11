from django.forms import ValidationError
from rest_framework import generics, response, status
from rest_framework.decorators import api_view
from gameusers.models import GameUser
from gameusers.serializers import UserSerializer
import uuid

# 매칭 유저 추가
class UserCreateView(generics.CreateAPIView):
    queryset = GameUser.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # save() 메서드 호출
        serializer.save()

        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
