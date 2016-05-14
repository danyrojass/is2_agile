# -*- encoding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from agileApp.models import Usuarios, Permisos, Roles, Permisos_Roles, Proyectos, Roles_Usuarios_Proyectos,\
Usuarios_Proyectos, User_Story, US_Proyectos, Sprint, Sprint_Proyectos, Flujos, Flujos_Proyectos, Actividades,\
Actividades_Flujos


class Command(BaseCommand):

    def handle(self, *args, **options):
        
        nombres = ['Administración de Usuarios', 'Administración de Proyectos/Servicios', 'Ver Página de Administración',
                   'Definición de Proyectos/Servicios', 'Asignación de Usuarios', 'Administración de Roles y Permisos', 
                   'Creación de US', 'Asignación de Roles', 'Modificación de US - Valores de Negocios', 
                   'Modificación de US - Valor Técnico','Modificación de US - Size', 'Modificación de US - Prioridad',
                   'Eliminación de US', 'Administración de Sprints', 'Administración de Flujos',
                   'Consultar lista de Usuarios', 'Cambiar Estado del Usuario', 'Asignación de US',
                   'Desarrollo de US',
                   'Consultar lista de Proyectos/Servicios', 'Modificación de US - Notas', 'Modificación de US - Archivos adjuntos',
                   'Modificación de US - Descripción', 'Consultar estado de Actividades', 'Consultar Recursos Disponibles', 
                   'Modificación de US - Tipo', 'Modificación de US - Tiempo Estimado', 'Modificación de US - Tiempo Real',  
                   'Consultar Historial del Proyecto/Servicio', 'Generar Burn Down Chart', 'Generar listado de US']
   
        niveles = [0, 0, 0,
                   1, 1, 1, 
                   1, 1, 1,
                   1, 1, 1,
                   1, 1, 1,
                   1, 1, 1,
                   2,
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
        u3 = crear_usuario('Usuario', 'Prueba1', 'uprueba1', 'a123', 'usuario_prueba1@gmail.com', True)
        u4 = crear_usuario('Usuario', 'Prueba2', 'uprueba2', 'a123', 'usuario_prueba2@gmail.com', True)
        u5 = crear_usuario('Usuario', 'Prueba3', 'uprueba3', 'a123', 'usuario_prueba3@gmail.com', True)
        u6 = crear_usuario('Daniel', 'Rojas', 'drojas', 'a123', 'danyrojassimon@gmail.com', True)
        u7 = crear_usuario('Luis', 'Soto', 'lsoto', 'a123', 'lutyma89@gmail.com', True)
        u8 = crear_usuario('Usuario', 'Prueba4', 'uprueba4', 'a123', 'usuario_prueba4@gmail.com', True)
        u9 = crear_usuario('Usuario', 'Prueba5', 'uprueba5', 'a123', 'usuario_prueba5@gmail.com', True)
        u10 = crear_usuario('Usuario', 'Prueba6', 'uprueba6', 'a123', 'usuario_prueba6@gmail.com', True)
        
        proyecto1 = crear_proyecto("Proyecto de Prueba Nro. 1", "Proy1", "Escenario de prueba 1.")
        proyecto2 = crear_proyecto("Proyecto de Prueba Nro. 2", "Proy2", "Escenario de prueba 2.")
        
        asignar_usuarios()
        
        us1 = crear_us("US de Prueba Nro.1", "Escenario de prueba 1.", 1, 2, 3, 4, u2)
        us2 = crear_us("US de Prueba Nro.2", "Escenario de prueba 2.", 2, 4, 6, 8, u3)
        us3 = crear_us("US de Prueba Nro.3", "Escenario de prueba 3.", 3, 4, 5, 6, u4)
        us4 = crear_us("US de Prueba Nro.4", "Escenario de prueba 4.", 1, 2, 3, 4, u7)
        us5 = crear_us("US de Prueba Nro.5", "Escenario de prueba 5.", 2, 4, 6, 8, u8)
        us6 = crear_us("US de Prueba Nro.6", "Escenario de prueba 6.", 3, 4, 5, 6, u9)
        
        asignar_us_proyecto(us1, proyecto1)
        asignar_us_proyecto(us2, proyecto1)
        asignar_us_proyecto(us3, proyecto1)
        asignar_us_proyecto(us4, proyecto2)
        asignar_us_proyecto(us5, proyecto2)
        asignar_us_proyecto(us6, proyecto2)
        
        sp1 = crear_sprint("Sprint de Prueba Nro.1", 150, 1)
        sp2 = crear_sprint("Sprint de Prueba Nro.2", 200, 1)
        
        asignar_sprint_proyecto(sp1, proyecto1)
        asignar_sprint_proyecto(sp2, proyecto2)
        
        f1 = crear_sprint("Flujo de Prueba Nro.1", "Escenario de prueba Nro.1")
        f2 = crear_sprint("Flujo de Prueba Nro.2", "Escenario de prueba Nro.1")
        
        asignar_flujo_proyecto(f1, proyecto1)
        asignar_flujo_proyecto(f2, proyecto2)
        
        act1 = crear_actividades("Actividad de Prueba Nro.1", "Escenario de prueba Nro.1")
        act2 = crear_actividades("Actividad de Prueba Nro.2", "Escenario de prueba Nro.2")
        
        asignar_actividad_flujo(act1, f1)
        asignar_actividad_flujo(act2, f2)

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
        permisos = Permisos.objects.all().exclude(nivel=0).exclude(nivel=1)
    
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
        
        if idx >=5:
            up = Usuarios_Proyectos(usuarios=usuario, proyecto=proyecto2)
            up.save()
            
            if idx == 5:
                rup = Roles_Usuarios_Proyectos(usuarios=usuario, roles=rol1, proyecto=proyecto2)
            else:
                rup = Roles_Usuarios_Proyectos(usuarios=usuario, roles=rol2, proyecto=proyecto2)
            rup.save()
            
        else:
            up = Usuarios_Proyectos(usuarios=usuario, proyecto=proyecto1)
            up.save()
            
            if idx == 0:
                rup = Roles_Usuarios_Proyectos(usuarios=usuario, roles=rol1, proyecto=proyecto1)
            else:
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

def crear_sprint(nombre, duracion, estado):
    sp = Sprint()
    sp.nombre = nombre
    sp.duracion = duracion
    sp.estado = estado
    sp.save()
    return sp
    
def asignar_sprint_proyecto(sprint, proyecto):
    sprint_proy = Sprint_Proyectos(proyecto=proyecto, sprint=sprint)
    sprint_proy.save()
    
def crear_flujo(nombre, descripcion):
    flujo = Flujos()
    flujo.nombre = nombre
    flujo.descripcion = descripcion
    flujo.estado = True
    flujo.save()
    return flujo

def asignar_flujo_proyecto(flujo, proyecto):
    flujo_proy = Flujos_Proyectos(proyecto=proyecto, flujo=flujo)
    flujo_proy.save()
    
def crear_actividades(nombre, descripcion):
    actividad = Actividades()
    actividad.nombre = nombre
    actividad.descripcion = descripcion
    actividad.save()
    
def asignar_actividad_flujo(actividad, flujo):
    act_flujo = Actividades_Flujos(actividad=actividad, flujo=flujo)
    act_flujo.save()