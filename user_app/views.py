from config.utils.response import success_response, error_response
from .serializers import UserSerializer
from .models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from django.shortcuts import render
from drf_spectacular.utils import extend_schema, extend_schema_view
from .permissions import IsRole


@extend_schema_view(
    get=extend_schema(
        description="Lista todos los usuarios registrados.",
        tags=["Usuarios"]
    ),
    post=extend_schema(
        description="Crea un nuevo usuario.",
        request=UserSerializer,
        responses={201: UserSerializer},
        tags=["Usuarios"]
    )
)
# Create your views here.
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        users = self.get_queryset()
        serializer = self.get_serializer(users, many=True)
        return Response(success_response(serializer.data, 'Usuarios listados'))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(success_response(serializer.data, 'Usuario creado'), status=status.HTTP_201_CREATED)
        return Response(error_response(serializer.errors, 'Error al crear usuario'), status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    get=extend_schema(
        description="Obtiene los datos de un usuario por su ID.",
        tags=["Usuarios"]
    ),
    patch=extend_schema(
        description="Actualiza parcialmente los datos de un usuario.",
        request=UserSerializer,
        tags=["Usuarios"]
    ),
    delete=extend_schema(
        description="Elimina un usuario por ID.",
        tags=["Usuarios"]
    )
)
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsRole]

    # Define los roles permitidos para esta vista
    allowed_roles = ['developer', 'admin']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(success_response(serializer.data, 'Usuario encontrado'))

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(success_response(serializer.data, 'Usuario actualizado'))
        return Response(error_response(serializer.errors, 'Error al actualizar usuario'), status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(success_response(message='Usuario eliminado'))
