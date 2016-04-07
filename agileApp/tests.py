from django.test import TestCase
from django.contrib.auth.models import User, AnonymousUser
from django.test.client import Client
from django.contrib.auth import authenticate, login
from django.test.client import Client, RequestFactory
from django.test import TestCase, RequestFactory

class test_templates(TestCase):
    
    def setUp(self):
        self.client = Client()
    
    
    def test_ver_adminPage(self):
        """
        Prueba de visualizacion del template de Pagina Admin
        """
        self.factory = RequestFactory()
        resp= self.factory.get('/templates/inicio_admin')
        self.assertTemplateUsed('inicio_admin.html')
    
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