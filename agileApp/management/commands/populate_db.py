# -*- encoding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def handle(self, *args, **options):
        crear_usuario('Alfredo', 'Barrios', 'abarrios', 'a123', 'alfbarrios2010@gmail.com', True)
        crear_usuario('Christian', 'Pérez', 'cperez', 'a123', 'criper123@gmail.com', True)
        crear_usuario('Luis', 'Soto', 'lsoto', 'a123', 'lutyma89@gmail.com', False)
        crear_usuario('Jorge', 'Rojas', 'jrojas', 'a123', 'danyrojassimon@gmail.com', False)
        
def crear_usuario(nombre, apellido, username, password, email, activo):
    user = User()
    user.first_name = nombre
    user.last_name = apellido
    user.username = username
    user.set_password(password)
    user.email = email
    user.is_active = activo
    user.save()
    return user