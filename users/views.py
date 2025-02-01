from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics

from users.models import User
from users.permissions import IsSelf
from users.serializers import UserSerializer, UserSelfSerializer


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSelfSerializer
    permission_classes = [IsAuthenticated, IsSelf]


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSelfSerializer
    permission_classes = [IsAuthenticated, IsSelf]


class UserDestroyAPIView(generics.DestroyAPIView):
    pass
    # queryset = User.objects.all()
    # serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]
