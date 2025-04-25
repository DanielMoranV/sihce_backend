from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer
from config.utils.response import success_response, error_response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample


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
            return Response(success_response(
                data=serializer.validated_data,
                message='Inicio de sesión exitoso'
            ), status=status.HTTP_200_OK)

        return Response(error_response(
            errors=serializer.errors,
            message='Error al iniciar sesión'
        ), status=status.HTTP_400_BAD_REQUEST)
