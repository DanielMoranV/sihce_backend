from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from user_app.models import User


class LoginSerializer(serializers.Serializer):
    dni = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        dni = attrs.get('dni')
        password = attrs.get('password')
        user = authenticate(dni=dni, password=password)
        if not user:
            raise serializers.ValidationError('Credenciales incorrectas')
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'role': user.role.name,
            'user': {
                'id': user.id,
                'dni': user.dni,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone': user.phone,
                'address': user.address,
                'role': user.role.name,
                'is_active': user.is_active,
            }
        }
