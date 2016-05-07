# -*- encoding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from agileApp.models import Usuarios, Permisos, Roles, Permisos_Roles, Proyectos, Roles_Usuarios_Proyectos,\
Usuarios_Proyectos, User_Story, US_Proyectos


class Command(BaseCommand):

    def handle(self, *args, **options):
        
        nombres = ['Administración de Usuarios', 'Administración de Proyectos/Servicios', 'Ver Página de Administración',
                   'Definición de Proyectos/Servicios', 'Asignación de Usuarios', 'Administración de Roles y Permisos', 
                   'Creación de US', 'Asignación de Roles', 'Modificación de US - Valores de Negocios', 
                   'Modificación de US - Valor Técnico','Modificación de US - Size', 'Modificación de US - Prioridad',
                   'Eliminación de US', 'Administración de Sprints', 'Administración de Flujos',
                   'Consultar lista de Usuarios', 'Cambiar Estado del Usuario', 'Desarrollo de US',
                   'Consultar lista de Proyectos/Servicios', 'Modificación de US - Notas', 'Modificación de US - Archivos adjuntos',
                   'Modificación de US - Descripción', 'Consultar estado de Actividades', 'Consultar Recursos Disponibles', 
                   'Modificación de US - Tipo', 'Modificación de US - Tiempo Estimado', 'Modificación de US - Tiempo Real',  
                   'Consultar Historial del Proyecto/Servicio', 'Generar Burn Down Chart', 'Generar listado de US']
   
        niveles = [0, 0, 0,
                   1, 1, 1, 
                   1, 1, 1,
                   1, 1, 1,
                   1, 1, 1,
                   1, 1, 2,
                   2, 2, 2,
                   2, 2, 2,
                   2, 2, 2,
                   3, 3, 3]
        c = 0
        for n in nombres:
            agregar_permisos(n, niveles[c])
            c = c + 1 

     
        crear_roles("Administrador", True, "Administrador del Sistema.")
        crear_roles("Scrum Master", True, "Líder del Proyecto.")
        crear_roles("Usuario Regular", False, "Soporte.")
        
        u1 = crear_usuario('Alfredo', 'Barrios', 'abarrios', 'a123', 'alfbarrios2010@gmail.com', True)
        u2 = crear_usuario('Christian', 'Pérez', 'cperez', 'a123', 'criper123@gmail.com', True)
        u3 = crear_usuario('Daniel', 'Rojas', 'drojas', 'a123', 'danyrojassimon@gmail.com', True)
        u4 = crear_usuario('Luis', 'Soto', 'lsoto', 'a123', 'lutyma89@gmail.com', True)
        u5 = crear_usuario('Usuario', 'Prueba', 'uprueba', 'a123', 'usuario_prueba@gmail.com', False)
        
        proyecto1 = crear_proyecto("Proyecto de Prueba Nro. 1", "Proy1", "Escenario de prueba 1.")
        proyecto2 = crear_proyecto("Proyecto de Prueba Nro. 2", "Proy2", "Escenario de prueba 2.")
        
        asignar_usuarios()
        
        us1 = crear_us("US de Prueba Nro.1", "Escenario de prueba 1.", 1, 2, 3, 4, u1)
        us2 = crear_us("US de Prueba Nro.2", "Escenario de prueba 2.", 4, 3, 2, 1, u2)
        
        asignar_us_proyecto(us1, proyecto1)
        asignar_us_proyecto(us2, proyecto2)

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
        rup = Roles_Usuarios_Proyectos(usuarios=usuario, roles=rol)
        rup.save()
        
    elif nombre=="Scrum Master":
        permisos = Permisos.objects.all().exclude(nivel=0)
    else:
        permisos = Permisos.objects.all().filter(nivel=3)
    
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
    return usuario
        
def agregar_permisos(nombre, nivel):
    permisos = Permisos()
    permisos.nombre = nombre
    permisos.nivel = nivel
    permisos.estado = True
    permisos.save()

def crear_proyecto(nombre_largo, nombre_corto, descripcion):
    proyecto = Proyectos()
    proyecto.nombre_largo = nombre_largo
    proyecto.nombre_corto = nombre_corto
    proyecto.descripcion = descripcion
    proyecto.save()
    return proyecto

def asignar_usuarios():
    usuarios = Usuarios.objects.all().exclude(id=1)
    rol1 = Roles.objects.get(nombre="Scrum Master")
    rol2 = Roles.objects.get(nombre="Usuario Regular")
    proyecto1 = Proyectos.objects.get(nombre_largo="Proyecto de Prueba Nro. 1")
    proyecto2 = Proyectos.objects.get(nombre_largo="Proyecto de Prueba Nro. 2")
    
    for idx, usuario in enumerate(usuarios):
        if idx == 0:

            up = Usuarios_Proyectos(usuarios=usuario, proyecto=proyecto1)
            up.save()
            
            rup = Roles_Usuarios_Proyectos(usuarios=usuario, roles=rol1, proyecto=proyecto1)
            rup.save()

        elif idx == 1:

            up = Usuarios_Proyectos(usuarios=usuario, proyecto=proyecto2)
            up.save()
            
            rup = Roles_Usuarios_Proyectos(usuarios=usuario, roles=rol2, proyecto=proyecto2)
            rup.save()
            
        elif idx == 2:

            
            up = Usuarios_Proyectos(usuarios=usuario, proyecto=proyecto2)
            up.save()
            
            rup = Roles_Usuarios_Proyectos(usuarios=usuario, roles=rol1, proyecto=proyecto2)
            rup.save()
            
        elif idx == 3:

            up = Usuarios_Proyectos(usuarios=usuario, proyecto=proyecto1)
            up.save()
            
            rup = Roles_Usuarios_Proyectos(usuarios=usuario, roles=rol2, proyecto=proyecto1)
            rup.save()

def crear_us(nombre, descripcion, nprioridad, vnegocios, vtecnico, size, user):
    uh = User_Story()
    uh.nombre = nombre
    uh.descripcion = descripcion
    uh.nivel_prioridad = nprioridad
    uh.valor_negocios = vnegocios
    uh.valor_tecnico = vtecnico
    uh.size = size
    uh.usuario_asignado = user
    uh.save()
    return uh

def asignar_us_proyecto(us, proyecto):
    us_proy = US_Proyectos(proyecto=proyecto, user_story=us)
    us_proy.save()