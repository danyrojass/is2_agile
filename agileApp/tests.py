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

from .models import Usuarios

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

class UsuarioTestCase(TestCase):
    
    def test_creacion_usuario(self):
        """
        Prueba la creacion de un usuario
        """
        #Se crea un usuario para la prueba
        us = User()
        us.username = "ariel"
        us.password = "ariel"
        us.email = "ariel@lastdeo.com"
        us.is_active = True
        us.save()
    
        #Se verifica si se ha creado el usuario, consultado si la
        #tabla usuario no esta vacia 
        self.assertTrue(User.objects.all() > 0, "No se ha guardado el usuario")
        
        
    def test_campos_obligatorios(self):
        """
        Se verifica que los campos obligatorios se han guardado
        """
        
        #Se crea un usuario para la prueba
        us = User()
        us.username = "alfredo"
        us.password = "alfbarrios123"
        us.email = "alfbarrios2010@gmail.com"
        us.is_active = True
        us.save()
    
        
        #Se obtienen los datos del usuario que se ha creado
        user = User.objects.get(username = "alfredo")
            
        #Se verifica si se han almacenado los campos obligatorios
        
        #Nombre de usuario 
        self.assertEqual(user.username, "alfredo", "No existe el usuario alfredo")
        #E-mail
        self.assertEqual(user.email, "alfbarrios2010@gmail.com", "No se ha guardado el email")
        #Contraseña
        self.assertEqual(user.password, "alfbarrios123", "No se ha guardado la contrasena")
    
  