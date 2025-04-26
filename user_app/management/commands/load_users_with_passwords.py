from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from user_app.models import User as CustomUser, Role


class Command(BaseCommand):
    help = 'Carga usuarios y les asigna contraseñas cifradas'

    def handle(self, *args, **kwargs):
        # Crear los usuarios
        users_data = [
            {
                "dni": "70315050",
                "first_name": "Daniel",
                "last_name": "Moran Vilchez",
                "email": "daniel.moranv94@gmail.com",
                "phone": "948860381",
                "address": "Sullana, Ignacio Escudero, 1",
                "is_superuser": True,
                "role": 1,
                "password": "admin3264"  # Aquí pones una contraseña de ejemplo
            },
            {
                "dni": "23456789",
                "first_name": "Ana",
                "last_name": "González",
                "email": "ana.gonzalez@example.com",
                "phone": "987654321",
                "address": "Avenida Principal 456",
                "role": 2,
                "password": "password456"
            },
            {
                "dni": "34567890",
                "first_name": "Carlos",
                "last_name": "Martínez",
                "email": "carlos.martinez@example.com",
                "phone": "1122334455",
                "address": "Calle Secundaria 789",
                "role": 3,
                "password": "password789"
            }
        ]

        for user_data in users_data:
            # Buscar el rol por su PK (ID)
            try:
                role = Role.objects.get(pk=user_data['role'])
            except Role.DoesNotExist:
                self.stdout.write(self.style.ERROR(
                    f"Rol con ID {user_data['role']} no encontrado"))
                continue  # Si no se encuentra el rol, pasa al siguiente usuario

            # Crear el usuario
            user = CustomUser(
                dni=user_data['dni'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                email=user_data['email'],
                is_superuser=user_data['is_superuser'] if 'is_superuser' in user_data else False,
                phone=user_data['phone'],
                address=user_data['address'],
                role=role
            )
            # Establecer la contraseña cifrada
            user.set_password(user_data['password'])
            user.save()  # Guardar el usuario
            self.stdout.write(self.style.SUCCESS(
                f"Usuario {user.dni} creado correctamente"))
