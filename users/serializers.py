from rest_framework.serializers import ModelSerializer

from materials.serializers import PaymentSerializer
from users.models import User


class UserSerializer(ModelSerializer):
    """
    Сериализатор для просмотра общей информации о пользователях.
    """

    class Meta:
        model = User
        fields = ("email", "is_active", "is_staff", "id", "city", "avatar")


class UserSelfSerializer(ModelSerializer):
    """
    Сериализатор для редактирования и просмотра собственного профиля.
    """

    payments = PaymentSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ("email", "city", "phone_number", "avatar", "payments")
