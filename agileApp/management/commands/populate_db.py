# -*- encoding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from sgpa2016.models import Usuarios, Permisos, Roles, Roles_Usuarios, Permisos_Roles

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        nombres = ['Administración de Usuarios', 'Administración de Proyectos/Servicios', 'Ver Página de Administración',
                   'Definición de Proyectos/Servicios', 'Asignación de Usuarios', 'Administración de Roles y Permisos', 
                   'Creación de US', 'Asignación de Roles', 'Modificación de US - Valores de Negocios', 
                   'Modificación de US - Valor Técnico','Modificación de US - Size', 'Modificación de US - Prioridad',
                   'Eliminación de US', 'Administración de Sprints', 'Administración de Flujos',
                   'Consultar lista de Usuarios', 
                   'Consultar lista de Proyectos/Servicios', 'Modificación de US - Notas', 'Modificación de US - Archivos adjuntos',
                   'Modificación de US - Descripción', 'Consultar estado de Actividades', 'Consultar Recursos Disponibles', 
                   'Consultar Historial del Proyecto/Servicio', 'Generar Burn Down Chart', 'Generar listado de US']
   
        niveles = [0, 0, 0,
                   1, 1, 1, 
                   1, 1, 1,
                   1, 1, 1,
                   1, 1, 1,
                   1, 
                   2, 2, 2,
                   2, 2, 2,
                   3, 3, 3]
        c = 0
        for n in nombres:
            agregar_permisos(n, niveles[c])
            c = c + 1 

     
        crear_roles("Administrador", True, "Administrador del Sistema.")
        crear_roles("Scrum Master", True, "Líder del Proyecto.")
        
        crear_usuario('Alfredo', 'Barrios', 'abarrios', 'a123', 'alfbarrios2010@gmail.com', True)
        crear_usuario('Christian', 'Pérez', 'cperez', 'a123', 'criper123@gmail.com', True)
        crear_usuario('Luis', 'Soto', 'lsoto', 'a123', 'lutyma89@gmail.com', True)
        crear_usuario('Daniel', 'Rojas', 'drojas', 'a123', 'danyrojassimon@gmail.com', False)

def crear_roles(nombre, tipo, observacion):
    rol = Roles()
    rol.nombre = nombre
    rol.tipo = tipo
    rol.estado = True
    rol.observacion = observacion
    rol.save()
    
    if nombre=="Administrador":       
        user = User.objects.get(pk=1)
        usuario = Usuarios()
        usuario.user = user
        usuario.save()
        permisos = Permisos.objects.all()
    
        ru = Roles_Usuarios()
        ru.usuario = usuario
        ru.roles = rol
        ru.save()
        
    else:
        permisos = Permisos.objects.all().exclude(nivel=0)
    
    for p in permisos:  
        pr = Permisos_Roles(permisos=p, roles=rol)
        pr.save()
        
def crear_usuario(nombre, apellido, username, password, email, activo):
    user = User()
    user.first_name = nombre
    user.last_name = apellido
    user.username = username
    user.set_password(password)
    user.email = email
    user.is_active = activo
    user.save()
    
    usuario = Usuarios()
    usuario.user = user
    usuario.save()
        
def agregar_permisos(nombre, nivel):
    permisos = Permisos()
    permisos.nombre = nombre
    permisos.nivel = nivel
    permisos.estado = True
    permisos.save()