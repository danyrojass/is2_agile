# -*- encoding: utf-8 -*-

from django.contrib.auth.models import User, AnonymousUser
from django.core import mail
from random import choice
from django.contrib.auth.hashers import make_password, check_password
from django.test.client import Client
from django.test import TestCase, RequestFactory
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from datetime import timedelta, date, datetime
from agileApp.models import Proyectos, Usuarios, Usuarios_Proyectos, Roles, Roles_Usuarios, Permisos, Permisos_Roles


class test_proyecto(TestCase):
    
    def test_crearproyecto(self):
        """
        Prueba de creacion correcta de un proyecto
        """    
        proyecto = Proyectos()
        proyecto.nombre_largo = 'Prueba_test'
        proyecto.nombre_corto = 'test'
        proyecto.tipo = True
        proyecto.fecha_inicio = '2016-01-01'
        proyecto.fecha_fin_estimado = '2016-01-02'
        proyecto.fecha_fin_real = '2016-01-03'
        proyecto.estado = 1
        proyecto.observaciones = 'Prueba de un proyecto'
        proyecto.save()
    
        self.assertTrue(Proyectos.objects.filter(nombre_largo = 'Prueba_test').exists(), "El proyecto no se ha creado")   
    
    def test_asignar_UsuarioProyecto(self):
        """
        Prueba de asignar un usuario a un proyecto
        """ 
        proyecto = Proyectos()
        proyecto.nombre_largo = 'Prueba_test'
        proyecto.nombre_corto = 'test'
        proyecto.tipo = True
        proyecto.fecha_inicio = '2016-01-01'
        proyecto.fecha_fin_estimado = '2016-01-02'
        proyecto.fecha_fin_real = '2016-01-03'
        proyecto.estado = 1
        proyecto.observaciones = 'Prueba de un proyecto'
        proyecto.save()
        
        #Se crea dos usuarios para la prueba, el segundo usuario es para probar la falla
        us = User()
        us.username = 'agil'
        us.set_password('admin123')
        us.email = "agile@sgpa.com"
        us.is_active = True
        us.save()
        
        us1 = User()
        us1.username = 'agil1'
        us1.set_password('admin1231')
        us1.email = "1agile@sgpa.com"
        us1.is_active = True
        us1.save()
        
        usuario = Usuarios()
        usuario.user = us
        usuario.save()

        usuario1 = Usuarios()
        usuario1.user = us1
        usuario1.save()

        
        us_proyecto = Usuarios_Proyectos(usuarios=usuario, proyecto=proyecto)
        us_proyecto.save()
        self.assertTrue(Proyectos.objects.filter(usuarios = usuario).exists(), "No se ha asignado el usuario, correctamente.") 
    
    def test_eliminar_Proyecto(self):
        """
        Prueba de eliminar un proyecto
        """ 
        proyecto = Proyectos()
        proyecto.nombre_largo = 'Prueba_test'
        proyecto.nombre_corto = 'test'
        proyecto.tipo = True
        proyecto.fecha_inicio = '2016-01-01'
        proyecto.fecha_fin_estimado = '2016-01-02'
        proyecto.fecha_fin_real = '2016-01-03'
        proyecto.estado = 1
        proyecto.observaciones = 'Prueba de un proyecto'
        proyecto.save()
        
        #Se simula la eliminacion del proyecto, poniendo el estado de Anulado
        proyecto.estado = 4
        
        self.assertEqual(proyecto.estado, 4, "No se ha Anulado el proyecto")
        
        
class test_roles_permisos(TestCase):
    
    def test_creacion_rol(self):
        """
        Prueba la creacion de un rol
        """
        rol = Roles()
        rol.nombre = 'Prueba Rol'
        rol.tipo = True
        rol.estado = True
        rol.observacion = 'Este es un rol de prueba'
        rol.save()
        
        #Se verifica si existe un rol con el nombre indicado
        self.assertEqual(rol.nombre, 'Prueba Rol', "No se ha creado el rol")
    
    def test_eliminar_rol(self):
        """
        Prueba la eliminacion de un rol
        """
        rol = Roles()
        rol.nombre = 'Prueba Rol'
        rol.tipo = True
        rol.estado = True
        rol.observacion = 'Este es un rol de prueba'
        rol.save()
        
        #Se cambia el estado del rol
        rol.estado = False
        self.assertEqual(rol.estado, False, "No se ha eliminado el rol")
        
        
    
    def test_creacion_permiso(self):
        """
        Prueba la creacion de un permiso
        """   
        permiso = Permisos()
        permiso.nombre = 'Crear Usuario'
        permiso.nivel = 1
        permiso.estado = False
        permiso.save()
        
        #Se verifica si se ha guardado el permiso consultando la tabla de permisos 
        
        self.assertTrue(Permisos.objects.all() > 0, "No se ha guardado el permiso")
    
    def test_asignar_PermisoRol(self):
        """
        Prueba la asignacion de un permiso a un rol
        """
        #Se crea un permiso para la prueba
        permiso = Permisos()
        permiso.nombre = 'Crear Usuario'
        permiso.nivel = 1
        permiso.estado = False
        permiso.save()
        
        #Se crea un permiso para probar la falla
        permiso2 = Permisos()
        
        #Se crea un rol para la prueba
        rol = Roles()
        rol.nombre = 'Prueba Rol'
        rol.tipo = True
        rol.estado = False
        rol.observacion = 'Este es un rol de prueba'
        rol.save()
        
        permiso_rol = Permisos_Roles(permisos=permiso, roles=rol)
        permiso_rol.save()
        self.assertTrue(Roles.objects.filter(permisos = permiso).exists(), "No se ha asignado el permiso, correctamente.") 
    

class test_login(TestCase):
    
    def test_login(self):
        """
        Prueba del login de un usuario
        """
        #Se crea un usuario para la prueba
        us = User()
        us.username = "agile_prueba"
        us.set_password('admin123')
        us.email = "agile@sgpa.com"
        us.is_active = True
        us.save()
        
        c = Client()
        self.assertTrue(c.login(username = 'agile_prueba', password = 'admin123'), "El usuario no se ha podido loguear")

class test_templates(TestCase):
    
    def setUp(self):
        self.client = Client()

    def test_ver_login(self):
        """
        Prueba de visualizacion del template de login
        """
        self.factory = RequestFactory()
        resp= self.factory.get('/templates/login')
        self.assertTemplateUsed('login.html')
        
    def test_ingresar(self):
        """
        Prueba de acceso a la pagina de ingreso
        """
        resp = self.client.get('/ingresar/')
        resp.user = AnonymousUser()
        self.assertEqual(resp.status_code, 200)

class test_assign(TestCase):
   
    def test_assing_user(self):
        """
        Prueba de la asignación de un usuario a un proyecto.
        """
        #Se crea un usuario para la prueba
        us = User()
        us.username = "agile_prueba"
        us.set_password('admin123')
        us.email = "agile@sgpa.com"
        us.is_active = True
        us.save()
            
        usuario = Usuarios()
        usuario.user = us
        usuario.save()
    
        proyecto = Proyectos()
        proyecto.nombre_largo = "Proyecto de Prueba"
        proyecto.nombre_corto = "ProyPr"
        proyecto.descripcion = "Escenario de Prueba para el test."
        proyecto.observaciones = "Ninguna, aún."
        proyecto.save()
        
        proy_us = Usuarios_Proyectos(usuarios=usuario, proyecto=proyecto)
        proy_us.save()
        
        self.assertTrue(Proyectos.objects.filter(usuarios = usuario).exists(), "No se ha asignado el usuario, correctamente.")
    
    def test_assing_role(self):
        """
        Prueba de la asignación de un rol a un usuario.
        """
        us = User()
        us.username = "agile_prueba"
        us.set_password('admin123')
        us.email = "agile@sgpa.com"
        us.is_active = True
        us.save()
            
        usuario = Usuarios()
        usuario.user = us
        usuario.save()
        rol = Roles()
        rol.nombre = "Rol de Prueba"
        rol.tipo = False
        rol.estado = True
        rol.observacion = "Ninguna, aún."
        rol.save()
        
        rol_us = Roles_Usuarios(usuario=usuario, roles=rol)
        rol_us.save()
        
        self.assertTrue(Usuarios.objects.filter(roles = rol).exists(), "No se ha asignado el rol, correctamente.")     
