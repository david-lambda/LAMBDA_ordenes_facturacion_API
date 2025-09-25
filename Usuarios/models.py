from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group

class UserManager(BaseUserManager):
    def create_user(self, correo, nombres, apellidos, password=None, **extra_fields):
        if not correo:
            raise ValueError('El usuario debe tener un correo electrónico.')
        if not nombres:
            raise ValueError('El usuario debe tener un nombre.')
        if not apellidos:
            raise ValueError('El usuario debe tener un apellido.')

        correo = self.normalize_email(correo)
        user = self.model(
            correo=correo,
            nombres=nombres,
            apellidos=apellidos,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, nombres, apellidos, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(correo, nombres, apellidos, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    correo = models.EmailField(verbose_name='Correo', max_length=255, unique=True)
    nombres = models.CharField(max_length=30, verbose_name='Nombres')
    apellidos = models.CharField(max_length=30, verbose_name='Apellidos')
    creado = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    modificado = models.DateTimeField(auto_now=True, verbose_name="Fecha de modificación")

    # Token para recuperación de contraseña
    reset_password_token = models.CharField(max_length=200, blank=True, null=True)
    reset_password_token_expires_at = models.DateTimeField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombres', 'apellidos']

    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.nombres} {self.apellidos}".title()

    def create_reset_token(self):
        self.reset_password_token = get_random_string(50)
        self.reset_password_token_expires_at = timezone.now() + timedelta(hours=1)
        self.save()

    def validate_reset_token(self, token):
        if (self.reset_password_token == token and 
            self.reset_password_token_expires_at and 
            timezone.now() < self.reset_password_token_expires_at):
            return True
        return False

    @property
    def is_staff(self):
        return self.is_superuser
