from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer
from config.utils.response import success_response, error_response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from user_app.serializers import UserSerializer


@extend_schema(
    request=LoginSerializer,
    responses={
        200: OpenApiExample(
            'Login Exitoso',
            value={
                'status': 'success',
                'message': 'Inicio de sesión exitoso',
                'data': {
                    'access': 'jwt-access-token',
                    'refresh': 'jwt-refresh-token',
                }
            },
            response_only=True
        ),
        400: OpenApiExample(
            'Error de Validación',
            value={
                'status': 'error',
                'message': 'Error al iniciar sesión',
                'errors': {
                    'dni': ['Este campo es obligatorio.'],
                    'password': ['Este campo es obligatorio.']
                }
            },
            response_only=True
        )
    },
    description="Permite iniciar sesión usando DNI y contraseña. Devuelve un token JWT.",
    tags=['Autenticación']
)
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            response = Response({
                "user": data["user"],
                "role": data["role"]
            }, status=status.HTTP_200_OK)

            # Acceso y refresh token como cookies seguras
            response.set_cookie(
                key='access_token',
                value=data['access'],
                httponly=True,
                secure=True,
                samesite='Lax',
                max_age=900  # 15 minutos
            )
            response.set_cookie(
                key='refresh_token',
                value=data['refresh'],
                httponly=True,
                secure=True,
                samesite='Lax',
                max_age=604800  # 7 días
            )
            return response
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
