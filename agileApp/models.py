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
   
"""
Clase Proyectos.
"""
class Proyectos(models.Model):
    nombre_largo = models.CharField(max_length=25, default="")
    nombre_corto = models.CharField(max_length=10, default="")
    tipo = models.BooleanField(default=True) #True: Proyecto. False: Servicio.
    descripcion = models.CharField(max_length=50, default="")
    fecha_inicio = models.DateField(default=timezone.now)
    fecha_fin_estimado = models.DateField(default=timezone.now)
    fecha_fin_real = models.DateField(default=timezone.now)
    observaciones = models.CharField(max_length=50, default="")
    estado = models.IntegerField(default=1) #1: Pendiente. 2: Anulado. 3: Activo. 4: Finalizado.
    usuarios = models.ManyToManyField(Usuarios, through='Usuarios_Proyectos')
    
    def __str__(self):
        return self.nombre_largo

class Roles_Usuarios(models.Model):
    roles = models.ForeignKey(Roles)
    usuario = models.ForeignKey(Usuarios)
    
class Usuarios_Proyectos(models.Model):
    proyecto = models.ForeignKey(Proyectos)
    usuarios = models.ForeignKey(Usuarios)

class Roles_Usuarios_Proyectos(models.Model):
    proyecto = models.ForeignKey(Proyectos)
    usuarios = models.ForeignKey(Usuarios)
    roles = models.ForeignKey(Roles)
