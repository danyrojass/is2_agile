"""
Modelos
"""
# -*- encoding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils import timezone

"""
Clase Permisos.
"""
class Permisos(models.Model):
    nombre = models.CharField(max_length=50, default="")
    nivel = models.IntegerField()
    estado = models.BooleanField(default=False)
    def __unicode__(self):
        return u"%s" % self.nombre

    def __str__(self):
        return self.nombre

"""
Clase Roles.
"""
class Roles(models.Model):
    nombre = models.CharField(max_length=25, default="")
    tipo = models.BooleanField(default=False) #True: Roles de Sistema. False: Roles de Usuario.
    estado = models.BooleanField(default=False)
    observacion = models.CharField(max_length=50, default="")
    permisos = models.ManyToManyField(Permisos, through='Permisos_Roles')
    
    def __unicode__(self):
        return u"%s" % self.nombre
    
    def __str__(self):
        return self.nombre
"""
Clase Usuarios.
"""
class Usuarios(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    telefono = models.CharField(max_length=15, default="")
    direccion = models.CharField(max_length=45, default="")
    tipo = models.CharField(max_length=10, default="")
    observacion = models.CharField(max_length=50, default="")
    roles = models.ManyToManyField(Roles, through='Roles_Usuarios')
    
    def __str__(self):
        return self.user.username

class Permisos_Roles(models.Model):
    permisos = models.ForeignKey(Permisos)
    roles = models.ForeignKey(Roles)
    
class Roles_Usuarios(models.Model):
    roles = models.ForeignKey(Roles)
    usuario = models.ForeignKey(Usuarios)