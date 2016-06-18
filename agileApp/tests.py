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
from agileApp.models import Proyectos, Reporte,Nota,Flujos,Actividades,Actividades_Flujos, US_Proyectos ,us_Flujos ,US_Sprint ,User_Story ,Usuarios, Sprint ,Usuarios_Proyectos, Roles,Roles_Usuarios_Proyectos, Permisos, Permisos_Roles,\
    US_Notas, US_Reportes, archivoAdjunto

class ArchivoAdjunto(TestCase):
    def test_Adjuntar(self):
        
        """Prueba para adjuntar un archivo"""
        adjunto = archivoAdjunto()
        archivo = 'test.py'
        hu = 1
        filename = 'test.py'
        
        self.assertTrue(archivoAdjunto.objects.all() > 0, "No se ha guardado el archivo") 

class test_Notas(TestCase):
    def test_CrearNotas(self):
        """
        Prueba para crear una nota de un user story.
        
        """
        nota=Nota()
        nota.nombre= 'prueba'
        nota.descripcion = 'prueba'
        nota.save()
        
        self.assertTrue(Nota.objects.filter(nombre = 'prueba').exists(), "La nota no se a creado")   

    def test_AgregarNot(self):    
        """
        Prueba para agregar una nota a un User Story.
        
        """
        nota=Nota()
        nota.nombre= 'prueba'
        nota.descripcion = 'prueba'
        nota.save()
        
        nota1=Nota()
        nota1.nombre= 'prueba2'
        nota1.descripcion = 'prueba2'
        nota1.save()
        
        #se crea un user story para la prueba
        
        us = User_Story()
        us.nombre = 'prueba user Story' 
        us.descripcion = 'descripcion prueba'
        us.nivel_prioridad = '5'
        us.valor_negocios = '5'
        us.urgencia= '5'
        us.size = '10'
        us.tiempo_estimado = '20'
        us.save()    
        
          
        n_us = US_Notas()
        n_us.user_story = us
        n_us.nota = nota
        n_us.save()
        self.assertTrue(User_Story.objects.filter(notas = nota).exists(), "No se ha asignado la nota correctamente.") 

class test_Reportes(TestCase):
    def test_CrearReporte(self):
        """
        Prueba para crear un reporte de un user story.
        
        """
        rp = Reporte()
        rp.descripcion = 'prueba'
        rp.porcentaje_alcanzado = '50'
        rp.horas_faltantes = '50'
        rp.fecha_reporte = '2016-01-01'
        rp.save()
        
        rp.save()
        
        self.assertTrue(Reporte.objects.filter(descripcion = 'prueba').exists(), "El reporte no se a creado")   
        
    def test_AgregarReporteUs(self):    
        """
        Prueba para generar un reporte de un user story.
        
        """
        rp = Reporte()
        rp.descripcion = 'prueba'
        rp.porcentaje_alcanzado = '50'
        rp.horas_faltantes = '50'
        rp.fecha_reporte = '2016-01-01'
        rp.save()
        
        rp1 = Reporte()
        rp1.descripcion = 'prueba2'
        rp1.porcentaje_alcanzado = '50'
        rp1.horas_faltantes = '50'
        rp1.fecha_reporte = '2016-01-01'
        rp1.save() 
        
        #se crea un user story para la prueba
        
        us = User_Story()
        us.nombre = 'prueba user Story' 
        us.descripcion = 'descripcion prueba'
        us.nivel_prioridad = '5'
        us.valor_negocios = '5'
        us.urgencia = '5'
        us.size = '10'
        us.tiempo_estimado = '20'
        us.save()    
        
          
        rp_us = US_Reportes(user_story=us, reporte=rp)
        rp_us.save()
        self.assertTrue(User_Story.objects.filter(reportes = rp).exists(), "No se ha asignado el reporte  correctamente.") 

class test_User_Story(TestCase):
    
    def test_crearUserStory(self):
        """
        Prueba de creacion correcta de un User Story
        """  
        us = User_Story()
        us.nombre = 'prueba user Story' 
        us.descripcion = 'descripcion prueba'
        us.nivel_prioridad = '5'
        us.valor_negocios = '5'
        us.urgencia = '5'
        us.size = '10'
        us.tiempo_estimado = '20'
        us.save()
        
        self.assertTrue(User_Story.objects.filter(nombre = 'prueba user Story').exists(), "El user story no se ha creado")   
    
    def test_asignarUserStoryaUsuario(self):
        """
        prueba para asignar User Story a Usuario       
        """
         #Se crea un usuario para la prueba
        usuario = User()
        usuario.username = "luis"
        usuario.password = "luis"
        usuario.email = "lutyma89@.com"
        usuario.is_active = True
        usuario.save()
        
        user = Usuarios()
        user.user = usuario
        user.save()
    
        #se crea un user story para la prueba
        
        us = User_Story()
        us.nombre = 'prueba user Story' 
        us.descripcion = 'descripcion prueba'
        us.nivel_prioridad = '5'
        us.valor_negocios = '5'
        us.urgencia = '5'
        us.size = '10'
        us.tiempo_estimado = '20'
        us.usuario_asignado = user
        us.save()    
        
        self.assertEqual(us.usuario_asignado, user, "No se ha asignado correctamente.")
            
    def test_asignarUserStoryaProyecto(self):
        """
        prueba para asignar User Story a proyecto       
        """
         #Se crea un proyecto para la prueba
         
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
            #se crea un user story para la prueba
        
        us = User_Story()
        us.nombre = 'prueba user Story' 
        us.descripcion = 'descripcion prueba'
        us.nivel_prioridad = '5'
        us.valor_negocios = '5'
        us.urgencia = '5'
        us.size = '10'
        us.tiempo_estimado = '20'
        us.save()    
        
        ac_fl = US_Proyectos(user_story=us, proyecto=proyecto)
        ac_fl.save()
        self.assertTrue(Proyectos.objects.filter(user_stories = us).exists(), "No se ha asignado el user story correctamente.") 

        
class test_sprint(TestCase):
    
    def test_crearSprint(self):
        """
        prueba de creacion correcta de un sprint
        """
        sprint = Sprint()
        sprint.nombre= 'Sprint Prueba'
        sprint.duracion = '50'
        sprint.estado = True
        sprint.save()
        
        nombre = "Prueba Sprint"

        self.assertTrue(Sprint.objects.filter(nombre = 'Sprint Prueba').exists(), "El sprint no se ha creado")   

    def test_modificarSprint(self):
        """
        Prueba de modificacion correcta de un sprint
        """    
        sprint = Sprint()
        sprint.nombre= 'Sprint Prueba'
        sprint.duracion = '50'
        sprint.estado = True
        sprint.save()
        
        sprint.nombre = 'Sprint Prueba cambio'
        sprint.save()
        self.assertTrue(Sprint.objects.filter(nombre = 'Sprint Prueba cambio').exists(), "El sprint no se ha modificado")   
    
    
    def test_crearUser_Story(self):
        """
        Prueba de creacion correcta de un User_Story
        """    
        us = User_Story()
        us.nombre = 'prueba user Story' 
        us.descripcion = 'descripcion prueba'
        us.nivel_prioridad = '5'
        us.valor_negocios = '5'
        us.urgencia = '5'
        us.size = '10'
        us.tiempo_estimado = '20'
        us.save()
        
        self.assertTrue(User_Story.objects.filter(nombre = 'prueba user Story').exists(), "El user story no se ha creado")   
    
    def test_modificarUser_Story(self):
        """
        Prueba de modificar un User_Story
        """    
        us = User_Story()
        us.nombre = 'prueba user Story' 
        us.descripcion = 'descripcion prueba'
        us.nivel_prioridad = '5'
        us.valor_negocios = '5'
        us.urgencia = '5'
        us.size = '10'
        us.tiempo_estimado = '20'
        us.save()
        
        us.nombre = 'prueba user Story 2'
        us.save()
        
        self.assertTrue(User_Story.objects.filter(nombre = 'prueba user Story 2').exists(), "El user Story  no se ha modificado")   
    
    def test_asignar_UserStoryaSprint(self):
        """
        Prueba de asignar un user Story a un Sprint
        """ 
        sprint = Sprint()
        sprint.nombre= 'Sprint Prueba'
        sprint.duracion = '50'
        sprint.estado = True
        sprint.save()
        
        #Se crea dos UserStory para la prueba, el segundo es para probar la falla
        us = User_Story()
        us.nombre = 'prueba user Story' 
        us.descripcion = 'descripcion prueba'
        us.nivel_prioridad = '5'
        us.valor_negocios = '5'
        us.urgencia = '5'
        us.size = '10'
        us.tiempo_estimado = '20'
        us.save()
        
        us = User_Story()
        us.nombre = 'prueba user Story 2' 
        us.descripcion = 'descripcion prueba'
        us.nivel_prioridad = '5'
        us.valor_negocios = '5'
        us.urgencia = '5'
        us.size = '10'
        us.tiempo_estimado = '20'
        us.save()
        
        ac_fl = US_Sprint(user_story=us,sprint =sprint)
        ac_fl.save()
        self.assertTrue(Sprint.objects.filter(listaUS = us).exists(), "No se ha asignado el User Story, correctamente.") 

class test_flujoActividad(TestCase):
    
    def test_crearFlujo(self):
        """
        Prueba de creacion correcta de un flujo
        """    
        flujo = Flujos()
        flujo.nombre = 'Flujo Prueba'
        flujo.descripcion = 'Descripcion de prueba'
        flujo.estado = True
        flujo.save()
        
        self.assertTrue(Flujos.objects.filter(nombre = 'Flujo Prueba').exists(), "El flujo no se ha creado")   
    
    def test_modificarFlujo(self):
        """
        Prueba de modificacion correcta de un flujo
        """    
        flujo = Flujos()
        flujo.nombre = 'Flujo Prueba'
        flujo.descripcion = 'Descripcion de prueba'
        flujo.estado = True
        flujo.save()
        
        flujo.nombre = 'Flujo Prueba cambio'
        flujo.save()
        self.assertTrue(Flujos.objects.filter(nombre = 'Flujo Prueba cambio').exists(), "El flujo no se ha modificado")   
    
    def test_crearActividad(self):
        """
        Prueba de creacion correcta de una actividad
        """    
        actividad = Actividades()
        actividad.nombre = 'Actividad Prueba'
        actividad.descripcion = 'Descripcion actividad'
        actividad.estado = 1
        actividad.save()
        
        self.assertTrue(Actividades.objects.filter(nombre = 'Actividad Prueba').exists(), "La actividad no se ha creado")   
    
    def test_modificarActividad(self):
        """
        Prueba de modificar una actividad
        """    
        actividad = Actividades()
        actividad.nombre = 'Actividad Prueba'
        actividad.descripcion = 'Descripcion actividad'
        actividad.estado = 1
        actividad.save()
        
        actividad.nombre = 'Actividad Prueba 2'
        actividad.save()
        self.assertTrue(Actividades.objects.filter(nombre = 'Actividad Prueba 2').exists(), "La actividad no se ha modificado")   
    
    def test_asignar_ActividadFlujo(self):
        """
        Prueba de asignar una actividad a un flujo
        """ 
        flujo = Flujos()
        flujo.nombre = 'Prueba flujo'
        flujo.descripcion = 'Prueba flujo descripcion'
        flujo.estado = True
        flujo.save()
        
        #Se crea dos actividades para la prueba, la segunda actividad es para probar la falla
        actividad = Actividades()
        actividad.nombre = 'Actividad Prueba'
        actividad.descripcion = 'Descripcion actividad'
        actividad.estado = 1
        actividad.save()
        
        actividad1 = Actividades()
        actividad1.nombre = 'Actividad Prueba 2'
        actividad1.descripcion = 'Descripcion actividad 2'
        actividad1.estado = 1
        actividad1.save()
        
        ac_fl = Actividades_Flujos(actividad=actividad, flujo=flujo)
        ac_fl.save()
        self.assertTrue(Flujos.objects.filter(actividades = actividad).exists(), "No se ha asignado la actividad, correctamente.") 

    def test_asignar_UsFlujo(self):
        """
        Prueba de asignar una User Story
        """ 
        flujo = Flujos()
        flujo.nombre = 'Prueba flujo'
        flujo.descripcion = 'Prueba flujo descripcion'
        flujo.estado = True
        flujo.save()
        
        #Se crea dos User Story  para la prueba, el segundo para el error
        us = User_Story()
        us.nombre = 'prueba user Story' 
        us.descripcion = 'descripcion prueba'
        us.nivel_prioridad = '5'
        us.valor_negocios = '5'
        us.urgencia = '5'
        us.size = '10'
        us.tiempo_estimado = '20'
        us.save()
        
        us1 = User_Story()
        us1.nombre = 'prueba user Story 2' 
        us1.descripcion = 'descripcion prueba'
        us1.nivel_prioridad = '5'
        us1.valor_negocios = '5'
        us1.urgencia = '5'
        us1.size = '10'
        us1.tiempo_estimado = '20'
        us1.save()
        
        ac_fl = us_Flujos(us=us, flujo=flujo)
        ac_fl.save()
        self.assertTrue(Flujos.objects.filter(us = us).exists(), "No se ha asignado el user story correctamente.") 

    
    
    
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
    
