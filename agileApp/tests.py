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
from .models import Usuarios, Roles, Roles_Usuarios, Proyectos, Usuarios_Proyectos
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