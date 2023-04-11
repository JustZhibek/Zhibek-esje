from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from .models import ConfirmUser


class UserLoginValidateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate_password(self, password):
        return password

class UserCreateValidateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    is_active = serializers.BooleanField(default=False, required=False)

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError('User already exists!')


class ConfirmUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.CharField(min_length=6, max_length=6)

    def validate_user_id(self, user_id):
        try:
            ConfirmUser.objects.get(id=user_id)
        except ConfirmUser.DoesNotExist:
            return user_id
        raise ValidationError("User_id does not exists!")