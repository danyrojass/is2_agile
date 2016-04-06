# -*- encoding: utf-8 -*-
import os
import sys


def start_populating(tipoAmbiente, nombreTag):
    
    if(tipoAmbiente==1):
        
        os.system("source ../agileEnv/bin/activate")
        os.system("python ../manage.py runserver")







    






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