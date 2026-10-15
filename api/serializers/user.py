from rest_framework import serializers

from ..models import CustomUser


class GetCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "date_joined",
            "first_name",
            "last_name",
            "last_login",
            "is_active",
            "is_staff",
            "is_superuser",

            "full_name",
            "phone_number",
            "date_of_birth",
        ]


class CreateCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "password", "email"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class UpdateCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "full_name",
            "email",
            "phone_number",
            "date_of_birth",
        ]
        extra_kwargs = {
            "full_name": {"write_only": True},
            "email": {"write_only": True},
            "phone_number": {"write_only": True},
            "date_of_birth": {"write_only": True},
        }

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class GetMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "full_name",
            "email",
            "phone_number",
            "date_of_birth",
        ]


class LoginCustomUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
