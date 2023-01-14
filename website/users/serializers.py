from rest_framework.serializers import ModelSerializer, EmailField, CharField
from rest_framework.validators import UniqueValidator

from .models import CustomUser


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "email", "password")


class RegistrationSerializer(ModelSerializer):
    email = EmailField(
        required=True,
        validators=[
            UniqueValidator(
                message="This email address is already registered.",
                queryset=CustomUser.objects.all(),
            )
        ],
    )
    username = CharField(
        validators=[
            UniqueValidator(
                message="This username is already registered.",
                queryset=CustomUser.objects.all(),
            )
        ]
    )
    password = CharField(min_length=8)

    class Meta:
        model = CustomUser
        fields = ("email", "username", "password")  # repeat password?
