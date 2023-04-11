from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserLoginValidateSerializer, UserCreateValidateSerializer
from django.contrib.auth.models import User
import random
from .models import ConfirmUser


@api_view(['POST'])
def authorization_api_view(request):
    serializer = UserLoginValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = authenticate(**serializer.validated_data)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'key': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED,
                    data={'error': 'Username or Password wrong!'})

@api_view(['POST'])
def registration_api_view(request):
    serializer = UserCreateValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = User.objects.create_user(**serializer.validated_data)
    code = ''.join([str(random.randrange(10)) for i in range(6)])
    cod = ConfirmUser.objects.create(user_id=user.id, code=code)
    return Response(status=status.HTTP_201_CREATED,
                    data={'user_id': user.id,
                          'code': cod.code})

@api_view(['POST'])
def confirm_api_view(request):
    serializer = ConfirmUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        if ConfirmUser.objects.filter(code=request.data['code']):
            User.objects.update(is_active=True)
            return Response(status=status.HTTP_200_OK,
                            data={'Ok!': 'User is active'})
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Code or id not found!'})
    except ValueError:
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                        data={'error': 'value error'})