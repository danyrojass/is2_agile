# -*- encoding: utf-8 -*-
import os
import sys
from django.contrib.auth.models import User

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

def start_populating(tipoAmbiente, nombreTag):
    
    if(tipoAmbiente==1):
        
        os.system("source ../agileEnv/bin/activate")
        
        crear_usuario('Alfredo', 'Barrios', 'abarrios', 'a123', 'alfbarrios2010@gmail.com', True)
        crear_usuario('Christian', 'Pérez', 'cperez', 'a123', 'criper123@gmail.com', True)
        crear_usuario('Luis', 'Soto', 'lsoto', 'a123', 'lutyma89@gmail.com', False)
        crear_usuario('Jorge', 'Rojas', 'jrojas', 'a123', 'danyrojassimon@gmail.com', False)
        
        os.system("python ../manage.py runserver")
        os.system("python ../deactivate")
    else:
        crear_usuario('Alfredo', 'Barrios', 'abarrios', 'a123', 'alfbarrios2010@gmail.com', True)
        crear_usuario('Christian', 'Pérez', 'cperez', 'a123', 'criper123@gmail.com', True)
        crear_usuario('Luis', 'Soto', 'lsoto', 'a123', 'lutyma89@gmail.com', False)
        crear_usuario('Jorge', 'Rojas', 'jrojas', 'a123', 'danyrojassimon@gmail.com', False)

if __name__ == '__main__':
    print "Populating the data base..."
    if(len(sys.argv)==3):
        ambiente=int(sys.argv[1])
        nombre=sys.argv[2]
        while(ambiente!=1 and ambiente !=2):
            ambiente=int(input("Ingrese 1 para ambiente Des o 2 para ambiente Pro: "))
    else:
        print len(sys.argv)
        print "La cantidad de argumentos no es válida!!!"
        
        ambiente=int(input("Ingrese 1 para ambiente Pro o 2 para ambiente Des: "))
        while(ambiente!=1 and ambiente !=2):
            ambiente=int(input("Ingrese 1 para ambiente Pro o 2 para ambiente Des: "))
        
        nombre=input("Ingrese el nombre del tag:")
    print ambiente
    start_populating(ambiente, nombre)
    print "We are Done... Thanks for wait :-)"