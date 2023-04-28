import jwt

from django.conf import settings

from rest_framework import views, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from users.models import User
from users.serializers import UserEmailSerializer, UserTokenSerializer


class UserEmailRegistration(generics.CreateAPIView):
    serializer_class = UserEmailSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        user_payload = {
            'user_id': user.id,
            'username': user.username
        }
        tokens = {
            'access_token': jwt.encode(user_payload, settings.SECRET_KEY, algorithm="HS256"),
            'refresh_token': jwt.encode(user_payload, settings.SECRET_KEY, algorithm="HS256")
        }
        return Response(
            tokens,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
