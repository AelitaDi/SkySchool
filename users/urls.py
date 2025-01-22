from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.apps import UsersConfig
from users.views import UserDestroyAPIView, UserCreateAPIView, UserUpdateAPIView, UserRetrieveAPIView, UserListAPIView

app_name = UsersConfig.name

# router = SimpleRouter()
# router.register("", UserViewSet)

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh"),
    path("", UserListAPIView.as_view(), name="users_list"),
    path("<int:pk>/", UserRetrieveAPIView.as_view(), name="user_retrieve"),
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("update/<int:pk>/", UserUpdateAPIView.as_view(), name="user_update"),
    path("delete/<int:pk>/", UserDestroyAPIView.as_view(), name="user_delete"),
]
# urlpatterns += router.urls
