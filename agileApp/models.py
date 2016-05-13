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
    horas_por_dia = models.IntegerField(null=True)
    roles = models.ManyToManyField(Roles, through='Roles_Usuarios_Proyectos')
    
    def __str__(self):
        return self.user.username

class Permisos_Roles(models.Model):
    permisos = models.ForeignKey(Permisos)
    roles = models.ForeignKey(Roles)


    
class Tipo(models.Model):
    nombre = models.CharField(max_length = 50, null=True)
    def __str__(self):
        return self.nombre

class User_Story(models.Model):
    nombre = models.CharField(max_length = 50, null = True)
    descripcion = models.CharField(max_length = 50, null = True)
    nivel_prioridad = models.IntegerField(null=True)
    valor_negocios = models.IntegerField(null=True)
    valor_tecnico = models.IntegerField(null=True)
    size = models.IntegerField(null=True)
    tiempo_estimado = models.IntegerField(default=0)
    tiempo_real = models.IntegerField(default=0)
    estado = models.IntegerField(default = 1)
    fecha_creacion = models.DateField(null = True)
    fecha_inicio = models.DateField(null = True)
    usuario_asignado = models.OneToOneField(Usuarios, null=True)
    tipo = models.OneToOneField(Tipo, null=True)
    id_flujo = models.IntegerField(null=True)
    id_sprint = models.IntegerField(null=True)
    f_estado = models.IntegerField(null=True) #1. To do. #2. Doing. #3. Done.
    f_actividad = models.IntegerField(null=True) #Nro. de actividad del flujo.
    def __str__(self):
        return self.nombre

class Actividades(models.Model):
    nombre = models.CharField(max_length=20, default="")
    descripcion = models.CharField(max_length=30, default="")
    estado = models.IntegerField(default=0) #0 = To Do, 1 = Doing, 2 = Done
    us = models.ManyToManyField(User_Story, through='us_Actividades')
    
class Sprint(models.Model):
    nombre=models.CharField(max_length=25, default="")
    duracion=models.IntegerField(default=0)
    estado=models.IntegerField(default=1)
    listaUS=models.ManyToManyField(User_Story,through='US_Sprint')

class Flujos(models.Model):
    nombre = models.CharField(max_length = 30, null = True)
    descripcion = models.CharField(max_length=50, default="")
    actividades = models.ManyToManyField(Actividades, through='Actividades_Flujos')
    tipo = models.OneToOneField(Tipo, null=True)
    estado = models.BooleanField(default=True)
    us = models.ManyToManyField(User_Story, through='us_Flujos')

class Actividades_Flujos(models.Model):
    flujo = models.ForeignKey(Flujos)
    actividad = models.ForeignKey(Actividades)    

class us_Flujos(models.Model):
    flujo = models.ForeignKey(Flujos)
    us = models.ForeignKey(User_Story)
    
class us_Actividades(models.Model):
    actividad = models.ForeignKey(Actividades)
    us = models.ForeignKey(User_Story)
    
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
    user_stories = models.ManyToManyField(User_Story, through='US_Proyectos')
    sprint = models.ManyToManyField(Sprint, through='Sprint_Proyectos')
    flujos = models.ManyToManyField(Flujos, through='Flujos_Proyectos')
    
    def __str__(self):
        return self.nombre_largo
    
class Usuarios_Proyectos(models.Model):
    proyecto = models.ForeignKey(Proyectos)
    usuarios = models.ForeignKey(Usuarios)

class Roles_Usuarios_Proyectos(models.Model):
    proyecto = models.ForeignKey(Proyectos, null=True)
    usuarios = models.ForeignKey(Usuarios)
    roles = models.ForeignKey(Roles)

class US_Proyectos(models.Model):
    proyecto = models.ForeignKey(Proyectos)
    user_story = models.ForeignKey(User_Story)

class Sprint_Proyectos(models.Model):
    proyecto = models.ForeignKey(Proyectos)
    sprint = models.ForeignKey(Sprint)

class US_Sprint(models.Model):
    sprint = models.ForeignKey(Sprint)
    user_story = models.ForeignKey(User_Story)

class Flujos_Proyectos(models.Model):
    proyecto = models.ForeignKey(Proyectos)
    flujo = models.ForeignKey(Flujos)
    