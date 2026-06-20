from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, documento, password=None,**extra_fields):
        if not documento:
            raise ValueError("Se requiere rellenar el campo del documento")
        
        email = extra_fields.pop('correo_electronico')
        email = self.normalize_email(email)
        usuario = self.model(documento=documento, correo_electronico=email, **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)
        
        return usuario
    
    def create_superuser(self, documento, password=None, **extra_fields):
        usuario = self.create_user(documento=documento, password=password, **extra_fields)
        usuario.is_staff=True
        usuario.is_superuser=True
        usuario.rol='ADMIN'
        usuario.save(using=self._db)
        return usuario
    
class Usuario(AbstractBaseUser,PermissionsMixin):

    TIPO_DOC_CHOICES = [('CC','CC'),('TI','TI')]
    ROL_CHOICES = [('ADMIN','Administrador'),('APRENDIZ','Aprendiz')]

    primer_nombre = models.CharField(max_length=45)
    segundo_nombre = models.CharField(max_length=45, blank=True, null=True)
    primer_apellido = models.CharField(max_length=45)
    segundo_apellido= models.CharField(max_length=45, blank=True, null=True)
    tipo_documento = models.CharField(max_length=2, choices=TIPO_DOC_CHOICES)
    documento = models.CharField(max_length=20, unique=True)
    celular = models.CharField(max_length=20)
    grupo_formacion = models.IntegerField(blank=True, null=True)
    correo_electronico = models.CharField(max_length=100, unique=True)
    rol = models.CharField(max_length=15, choices=ROL_CHOICES)
    tipo_apoyo = models.CharField(max_length=15)
    fecha_registro = models.DateField(auto_now_add=True)
    ultima_actualizacion = models.DateField(auto_now=True)

    USERNAME_FIELD = 'documento' #esto hace que se use el documento en luegar de username
    REQUIRED_FIELDS = ["primer_nombre", "primer_apellido", "tipo_documento", "celular", "correo_electronico"]

    objects = UserManager()

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.primer_nombre} {self.primer_apellido} - ({self.documento})"
