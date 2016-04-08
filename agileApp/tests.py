from django.contrib.auth.models import User, AnonymousUser
from django.core import mail
from random import choice
from django.contrib.auth.hashers import make_password, check_password
from django.test.client import Client
from django.test import TestCase, RequestFactory
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from datetime import timedelta, date, datetime

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
