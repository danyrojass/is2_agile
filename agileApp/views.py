# -*- encoding: utf-8 -*-
from django.shortcuts import get_object_or_404, render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.template import RequestContext
from datetime import datetime
from datetime import timedelta
from .forms import RegistroUserForm, EditarUserForm, BuscarUserForm, CrearRolForm, BuscarRolForm,\
EditarRolForm, ModificarContrasenaForm, CrearProyectoForm, DefinirProyectoForm, BuscarProyectoForm,\
EditarProyectoForm, AsignarRolForm, CambiarEstadoForm, CrearUSForm, BuscarUSForm, EditarUSForm, AsignarUSForm,\
BuscarSprintForm, CrearSprintForm, EditarSprintForm, CambiarEstadoUSForm , BuscarFlujosForm
from .models import Usuarios, Permisos, Roles, Permisos_Roles, Usuarios, Proyectos, Roles_Usuarios_Proyectos, Flujos_Proyectos,\
Usuarios_Proyectos, User_Story, US_Proyectos, Tipo, Sprint, Sprint_Proyectos, US_Sprint, Flujos, Actividades, Actividades_Flujos,\
us_Flujos, Usuarios_Sprint
from django.contrib.auth.hashers import make_password
from agileApp.forms import CambiarEstadoSprintForm, EditarActividadForm, EditarFlujoForm, CrearActividadForm,\
CrearFlujosForm, BuscarFlujoForm, CambiarEstadoFlujoForm, ReportarUSForm,archivoUSForm,\
    NotasUSForm, CambiarEstadoUSFlujoForm
from agileApp.models import Reporte, US_Reportes, Archivo, US_Archivos, Horas,\
    Nota, US_Notas
import math
 
def inicio(request): 
    """
    Ingreso al sistema.
    @param request: Http request
    @type  request:HtpptRequest 
    @return: render a index.html con el Usuario
    """    
    
    if request.user.is_anonymous():
        return HttpResponseRedirect('/ingresar')
    else:
        return HttpResponseRedirect('/index')

def ingresar(request):
    """
    Metodo que permite el inicio de sesion en el sistema.
    Verifica que el usuario este activo y lo redirige a su template correspondiente
    segun su rol en el sistema 
    
    @param request: Http request
    @type  request:HtpptRequest 
    @return: render a template correspondiente segun rol del usuario en el sistema, contexto
    """
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['last_activity'] = str(now)
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/index')
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)

                    return HttpResponseRedirect('/index')
                else:
                    return render_to_response('noactivo.html', context_instance=RequestContext(request))
            else:
                return render_to_response('nousuario.html', context_instance=RequestContext(request))
    else:
        formulario = AuthenticationForm()
        return render_to_response('login.html',{'formulario':formulario}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def cerrar(request):
    """
    Recibe un request y cierra la sesion correspondiente.
    
    @param request:Http request
    @type  request:HtpptRequest 
    @return: render al template de login
    
    """

    
    
    logout(request)
    return HttpResponseRedirect('/ingresar')

@login_required(login_url='/ingresar')
def index(request):
    """
    Método que verifica el tipo de usuario y lo redirige a su template correspondiente
    dependiendo si es es un tipo administrador o un usuario normal.
    
    @param request:Http request
    @type  request:HtpptRequest 
    @return: renderiza los datos del usuario con el template correspondiente.
    
    """
    
    comprobar(request)
    if(request.user.is_anonymous()):
        return HttpResponseRedirect('/ingresar')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['last_activity'] = str(now)
    
    usuario = request.user
    usuario_profile = Usuarios.objects.get(id=usuario.id)
    permiso = Permisos.objects.filter(nombre="Ver Página de Administración")
    rol = Roles.objects.filter(permisos=permiso)
    rol_usuario_profile = Usuarios.objects.get(roles=rol)
    saludo = saludo_dia()
        
    if usuario_profile == rol_usuario_profile:
        return render_to_response('inicio_admin.html', {'usuario':usuario, 'saludo':saludo}, context_instance=RequestContext(request))    
    else:
        proyectos = Proyectos.objects.filter(usuarios__id=usuario.id)

    if not proyectos:
        return render_to_response('noasignado.html', {'usuario':usuario, 'saludo':saludo}, context_instance=RequestContext(request))
    else:
        return render(request, 'elegir_proyecto.html', {'usuario':usuario, 'proyectos':proyectos, 'saludo':saludo})

def creditos(request):
    """
    Método que se encarga de mostrar los créditos del sistema.
    
    @param request:Http request
    @type  request:HtpptRequest
    @return: render al template de creditos.html
    
    """
    comprobar(request)
    if(request.user.is_anonymous()):
        return HttpResponseRedirect('/ingresar')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['last_activity'] = str(now)        
    usuario = request.user
    saludo = saludo_dia()
    
    staff=verificar_permiso(usuario, "Ver Index de Admin")
    
    return render_to_response('creditos.html', {'usuario':usuario, 'saludo':saludo, 'staff':staff}, context_instance=RequestContext(request))    

def index_usuarios(request):
    usuario = request.user
    accion = "Index de Usuarios"
    
    staff = verificar_permiso(usuario, accion)
    
    if staff:
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)

        saludo = saludo_dia()
        
        usuarios = User.objects.order_by('id')
        filas= usuarios.count() - 1
        
        if request.method == 'POST':
            results = Usuarios.objects.all().exclude(id=1)
            form = BuscarUserForm(request.POST)
            
            if form.is_valid():
                uid = request.POST.get('id', None)
                if uid:
                    if uid != usuario.id:
                        results = results.filter(id__iexact=uid)
                    else:
                        results = None
                        
                uusername = request.POST.get('username', None)
                if uusername:
                    if uusername != usuario.username:

                        results = results.filter(user__username__icontains=uusername)
                    else:
                        results = None
                        
                uemail = request.POST.get('email', None)
                if uemail:
                    if uemail != usuario.email:
                        results = results.filter(user__email__icontains=uemail)
                    else:
                        results = None
                        
                first_name = request.POST.get('first_name', None)
                if first_name:
                    if first_name != usuario.first_name:
                        results = results.filter(user__first_name__icontains=first_name)
                    else:
                        results = None
                        
                last_name = request.POST.get('last_name', None)
                if last_name:
                    if last_name != usuario.last_name:
                        results = results.filter(user__last_name__icontains=last_name)
                    else:
                        results = None
                
                utipo = request.POST.get('tipo', None)
                if utipo:
                        results = results.filter(tipo__iexact=utipo)
                        
                if not uid and not uusername and not uemail and not first_name and not last_name and not utipo:
                    results = None
                if results:
                    results.order_by('id')
                return render_to_response('usuarios/results.html', {'usuario':usuario, 'saludo':saludo, 'results':results}, context_instance=RequestContext(request))
        else:
            form = BuscarUserForm()
        
        return render(request, 'usuarios/index.html', {'usuario':usuario, 'saludo':saludo, 'usuarios':usuarios, 'filas':filas})
    else:
        return HttpResponseRedirect('/index')
    
@login_required(login_url='/ingresar')
def registrar_usuarios(request):
    """ 
    Registra a un Usuario al sistema.
    
    @param request:Http request
    @type  request:HtpptRequest
    @return: renderiza template registro.html
    
    
    """
    usuario = request.user
    accion = "Registro de Usuarios"
    
    staff = verificar_permiso(usuario, accion)
    
    if staff:
        aid = 1
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
        
        saludo = saludo_dia()
            
        if request.method == 'POST':
            form = RegistroUserForm(request.POST, request.FILES)
        
            if form.is_valid():
                cleaned_data = form.cleaned_data
                username = cleaned_data.get('username')
                password = cleaned_data.get('password')
                email = cleaned_data.get('email')
                first_name = cleaned_data.get('first_name')
                last_name = cleaned_data.get('last_name')
                telefono = cleaned_data.get('telefono')
                direccion = cleaned_data.get('direccion')
                tipo = cleaned_data.get('tipo')
                observacion = cleaned_data.get('observacion')
        
                user_model = User.objects.create_user(username=username, password=password)
                user_model.email = email
                user_model.first_name = first_name
                user_model.last_name = last_name
                user_model.is_active = True
                user_model.save()
                    
                user_profile = Usuarios()
                user_profile.user = user_model
                user_profile.id = user_model.id
                user_profile.telefono = telefono
                user_profile.direccion = direccion
                user_profile.tipo = tipo
                user_profile.observacion = observacion
                
                user_profile.save()
                return render_to_response('usuarios/gracias.html', {'usuario':usuario, 'saludo':saludo, 'um':user_model, 'up':user_profile, 'aid':aid}, context_instance=RequestContext(request))   
        else:
            form = RegistroUserForm()
        
        return render(request, 'usuarios/registro.html', {'usuario':usuario, 'saludo':saludo, 'form': form})
    else:
        return HttpResponseRedirect('/index')
    
@login_required(login_url='/ingresar')
def editar_usuarios(request, user_id):
    """ 
    Edita un Usuario del sistema.
    
    @param request:Http request
    @type  request:HtpptRequest
    @param user_id: Id de un usuario registrado  
    @return: renderiza template registro.html
    
    
    """
    usuario = request.user
    accion = "Editar Usuarios"
    accion2 = "Cambiar Estado"
    
    staff = verificar_permiso(usuario, accion)
    staff2 = verificar_permiso(usuario, accion2)
    
    if staff:
        
        aid = 2
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
        
        saludo = saludo_dia()
        
        user_model = get_object_or_404(User, pk=user_id)
        user_profile = get_object_or_404(Usuarios, id=user_id)
    
        if request.method == 'POST':
            form = EditarUserForm(request.POST, request.FILES)
            if form.is_valid():
                password = form.cleaned_data['password']
                if password:
                    user_model.password =  make_password(password)
                user_model.email = form.cleaned_data['email']
                user_model.first_name = form.cleaned_data['first_name']
                user_model.last_name = form.cleaned_data['last_name']  
                activo = form.cleaned_data['estado']
                if activo:
                    user_model.is_active = activo
                user_model.save()
                
                user_profile.telefono = form.cleaned_data['telefono']
                user_profile.direccion = form.cleaned_data['direccion']
                user_profile.observacion = form.cleaned_data['observacion']
                user_profile.save()
    
                return render_to_response('usuarios/gracias.html', {'usuario':usuario, 'saludo':saludo, 'aid':aid, 'um':user_model, 'up':user_profile}, context_instance=RequestContext(request))
        else:
            form = EditarUserForm()
        return render(request, 'usuarios/editar.html', {'form': form, 'usuario':usuario, 'saludo':saludo, 'um':user_model, 'up':user_profile})
    elif staff2:
        aid = 1
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
        
        saludo = saludo_dia()
        
        user_model = get_object_or_404(User, pk=user_id)
        user_profile = get_object_or_404(Usuarios, id=user_id)
    
        if request.method == 'POST':
            form = CambiarEstadoForm(request.POST, request.FILES)
            if form.is_valid():

                estado = form.cleaned_data['estado']
                user_model.is_active = estado
                user_model.save()
                if estado:
                    proyecto = Proyectos.objects.get(usuarios__id=user_model.id)
                    desasignar_usuarios(request, user_model.id, proyecto.id)
                return render_to_response('proyecto_usuario/gracias.html', {'usuario':usuario, 'saludo':saludo, 'aid':aid, 'um':user_model, 'up':user_profile}, context_instance=RequestContext(request))
        else:
            form = CambiarEstadoForm()
        return render(request, 'usuarios/editar.html', {'staff2':staff2, 'form': form, 'usuario':usuario, 'saludo':saludo, 'um':user_model, 'up':user_profile})
    else:
        return HttpResponseRedirect('/index')

def eliminar_usuarios(request, user_id):
    """ 
    Redirige a eliminar un Usuario del sistema.
    
    @param request:Http request
    @type  request:HtpptRequest
    @param user_id: Id de un usuario registrado  
    @return: renderiza y redirige al template eliminar.html
    
    
    """
    usuario = request.user
    accion = "Borrar Usuarios"
    
    staff = verificar_permiso(usuario, accion)
    
    if staff:
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)

        saludo = saludo_dia()
        
        user = get_object_or_404(User, pk=user_id)
        
        return render_to_response('usuarios/eliminar.html', {'usuario':usuario, 'saludo':saludo, 'user':user})
    else:
        return HttpResponseRedirect('/index')

@login_required(login_url='/ingresar')
def delete_usuarios(request, user_id):
    """ 
    Elimina a un Usuario del sistema, es decir lo pone en estado inactivo.
    
    @param request:Http request
    @type  request:HtpptRequest
    @param user_id: Id de un usuario registrado  
    @return: renderiza template gracias.html
    
    
    """
    usuario = request.user
    accion = "Borrar Usuarios"
    
    staff = verificar_permiso(usuario, accion)
    
    if staff:
        aid = 3

        saludo = saludo_dia()
           
        user_model = get_object_or_404(User, pk=user_id)
        user_profile = get_object_or_404(Usuarios, id=user_id)
        
        user_model.is_active = False
        user_model.save()    
        return render_to_response('usuarios/gracias.html', {'usuario':usuario, 'saludo':saludo, 'um':user_model, 'up':user_profile, 'aid':aid}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/index')
    
@login_required(login_url='/ingresar')
def modificar_contrasena(request):
    """
    Método que permite modificar la contraseña, del usuario solicitante.
    
    @param request: Http request
    @return: render al template usuarios/modificar_contrasena.html para la modificación. 
             render al template usuarios/gracias.html cuando se ha modificado correctamente.
    """
    aid = 4
    
    usuario = request.user
    user = User.objects.filter(id=usuario.id)
    saludo = saludo_dia()
    
    staff=verificar_permiso(usuario, "Ver Index de Admin")
    
    if request.method == 'POST':
        form = ModificarContrasenaForm(request.POST, user=user)
        if form.is_valid():
            usuario.password =  make_password(form.cleaned_data['password'])   
            usuario.save()

            return render_to_response('usuarios/gracias.html', {'aid':aid, 'usuario':usuario, 'saludo':saludo, 'staff':staff}, context_instance=RequestContext(request))
    else:
        form = ModificarContrasenaForm(user=user)
    return render(request, 'usuarios/modificar_contrasena.html', {'form': form, 'usuario':usuario, 'saludo':saludo,'staff':staff})

@login_required(login_url='/ingresar')
def ver_usuarios(request, user_id):
    """ 
    Muestra a un Usuario del sistema.
    
    @param request:Http request
    @type  request:HtpptRequest
    @param user_id: Id de un usuario registrado  
    @return: renderiza template ver.html
    
    
    """
    usuario = request.user
    accion = "Ver Usuarios"
    
    staff = verificar_permiso(usuario, accion)
    
    if staff:
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)

        saludo = saludo_dia()
        
        user_model = get_object_or_404(User, pk=user_id)
        user_profile = get_object_or_404(Usuarios, id=user_id)
        
        return render_to_response('usuarios/ver.html', {'usuario':usuario, 'saludo':saludo, 'um':user_model, 'up':user_profile})
    else:
        return HttpResponseRedirect('/index')


"""Administración de Roles"""
def crear_roles(request):
    """
    Método para la creación de roles con la asignación de sus permisos correspondientes.

    @param request:Http request
    @return:render a roles/crear.html que cuenta con las especificaciones para la creación del rol.

    """
    
    usuario = request.user
    accion = "Registro de Roles"
    
    staff = verificar_permiso(usuario, accion)
    
    if staff:
        aid = 1
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)

        saludo = saludo_dia()
            
        permisos1 = Permisos.objects.all().filter(nivel=1)
        permisos2 = Permisos.objects.all().filter(nivel=2)
        permisos3 = Permisos.objects.all().filter(nivel=3)
        permisos = map(None, permisos1, permisos2, permisos3)
                
        if request.method == 'POST':
            form = CrearRolForm(request.POST, request.FILES)
            
            if form.is_valid():
                cleaned_data = form.cleaned_data
                nombre = cleaned_data.get('nombre')
                tipo = cleaned_data.get('tipo')
                observacion = cleaned_data.get('observacion')
            
                rol = Roles()
                rol.nombre = nombre
                rol.tipo = tipo
                rol.observacion = observacion
                rol.estado = True
                rol.save()
                    
                rol_id = rol.id
                lista_permisos = request.POST.getlist(u'permisos')
                    
                asignar_permisos_rol(request, rol_id, lista_permisos)
                pr1 = rol.permisos.all().filter(nivel=1)
                pr2 = rol.permisos.all().filter(nivel=2)
                pr3 = rol.permisos.all().filter(nivel=3)
                pr = map(None, pr1, pr2, pr3)
                   
                return render_to_response('roles/gracias.html', {'aid':aid, 'usuario':usuario, 'saludo':saludo, 'pr':pr, 'rol':rol}, context_instance=RequestContext(request))
        else:
            form = CrearRolForm()
            
        return render(request, 'roles/crear.html', {'usuario':usuario, 'saludo':saludo, 'form': form, 'permisos':permisos})
    else:
        return HttpResponseRedirect('/index')
    
def asignar_permisos_rol(request, rol_id, lista_permisos):
    """
    Método para asignar los permisos con los que contara un rol.
   
   
    @param request:Http request
    @param user_id:Id de un rol existente en el sistema.
    @return: rol con los permisos asignados recientemente.

    """  

    rol = get_object_or_404(Roles, id=rol_id)
    
    for p in lista_permisos:
        
        permiso = Permisos.objects.get(pk=p)   
        pr = Permisos_Roles(permisos=permiso, roles=rol)
        pr.save()
       
    return pr

def editar_roles(request, rol_id):
    """
    Método que nos permite modificar un rol existente en el sistema.

    @param request: Http request
    @param role_id: Id de un rol registrado en el sistema
    @return: render a roles/editar.html con la descripción del rol modificado.

    """
    
    usuario = request.user
    accion = "Editar Roles"
    
    staff = verificar_permiso(usuario, accion)
    
    if staff:
        aid = 2
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
            
        saludo = saludo_dia()
        
        listax = []
   
        permisos1 = Permisos.objects.all().filter(nivel=1)
        permisos2 = Permisos.objects.all().filter(nivel=2)
        permisos3 = Permisos.objects.all().filter(nivel=3)
        permisos = map(None, permisos1, permisos2, permisos3)
            
        rol = get_object_or_404(Roles, id=rol_id)
        p1 = rol.permisos.all().filter(nivel=1)
        p2 = rol.permisos.all().filter(nivel=2)
        p3 = rol.permisos.all().filter(nivel=3)
        lista = map(None, p1, p2, p3)
        
        for p, q, r in lista:
            if not None:
                if p:
                    listax.append(p.nombre)
                if q:
                    listax.append(q.nombre)
                if r:
                    listax.append(r.nombre)
     
        if request.method == 'POST':
            form = EditarRolForm(request.POST, rol_id=rol_id)
            if form.is_valid():
                    rol.nombre = form.cleaned_data['nombre']
                    rol.tipo = form.cleaned_data['tipo']
                    rol.observacion = form.cleaned_data['observacion']
                    rol.save()
                    
                    rol_id = rol.id
                    lista_permisos = request.POST.getlist(u'permisos')
                    
                    editar_permisos_rol(request, rol_id, lista_permisos)
                    pr1 = rol.permisos.all().filter(nivel=1)
                    pr2 = rol.permisos.all().filter(nivel=2)
                    pr3 = rol.permisos.all().filter(nivel=3)
                    pr = map(None, pr1, pr2, pr3)
                    
                    return render_to_response('roles/gracias.html', {'aid':aid, 'usuario':usuario, 'saludo':saludo, 'pr':pr, 'rol':rol}, context_instance=RequestContext(request))
        else:
            form = EditarRolForm(rol_id=rol_id)
        return render(request, 'roles/editar.html', {'form': form, 'usuario':usuario, 'saludo':saludo, 'rol':rol, 'lista':lista, 'listax':listax, 'permisos':permisos})
    else:
        return HttpResponseRedirect('/index')
    
def editar_permisos_rol(request, rol_id, lista_permisos):
    """
    Nos permite modificar los permisos de un rol registrado en el sistema.
  
   
    @param request: Http request
    @param role_id: Id de un rol registrado en el sistema
    @return: render a roles/ver.html con sus respectivos permisos a modificar.

    """  
    
    rol = get_object_or_404(Roles, id=rol_id)
    rp = rol.permisos.all() 
    existe = False
    
    for pe in rp:
        for p in lista_permisos:
            if pe.id == p:
                existe = True
        if existe == False:
            permiso = get_object_or_404(Permisos, id=pe.id)
            roles = get_object_or_404(Roles, id=rol_id)
            permisosRoles = Permisos_Roles.objects.get(permisos=permiso, roles=roles)
            permisosRoles.delete()
        existe = False
            
    for p in lista_permisos:
        for pe in rp:
            if p != pe.id:         
                permiso = Permisos.objects.get(pk=p)   
                per = Permisos_Roles(permisos=permiso, roles=rol)
                per.save()
                break
       
    return per

def ver_roles(request, rol_id):
    """
    Nos permite ver los roles registrados en el sistema.
 
    
   @param request: Http request
   @param role_id: Id de un rol registrado en el sistema
   @return: render a roles/ver.html.

    """
    
    usuario = request.user
    accion = "Ver Roles"
    
    staff = verificar_permiso(usuario, accion)
    
    if staff:
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
            
        saludo = saludo_dia()
            
        rol = get_object_or_404(Roles, id=rol_id)
        permisos1 = rol.permisos.all().filter(nivel=1)
        permisos2 = rol.permisos.all().filter(nivel=2)
        permisos3 = rol.permisos.all().filter(nivel=3)
        pr = map(None, permisos1, permisos2, permisos3)
            
        return render_to_response('roles/ver.html', {'usuario':usuario, 'saludo':saludo, 'rol':rol, 'pr':pr})
    else:
        return HttpResponseRedirect('/index')
    
def eliminar_roles(request, rol_id):

    """
    Método para eliminar un rol existente del sistema.

   
    @param request: Http request
    @param role_id: Id de un rol registrado en el sistema
    @return: render a roles/eliminar.html.  

    """

    usuario = request.user
    accion = "Borrar Roles"
    
    staff = verificar_permiso(usuario, accion)
    
    if staff:
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
            
        usuario = request.user
        saludo = saludo_dia()
            
        rol = get_object_or_404(Roles, id=rol_id)
            
        return render_to_response('roles/eliminar.html', {'usuario':usuario, 'saludo':saludo, 'rol':rol})
    else:
        return HttpResponseRedirect('/index')
    
def delete_roles(request, rol_id):
    """
     Establece el estado de un rol a False
    @param request: Http request
    @param rol_id: Id de un rol registrado en el sistema
    @return:roles/gracias.html

    """
    
    usuario = request.user
    accion = "Borrar Roles"
    
    staff = verificar_permiso(usuario, accion)
    
    if staff:
        aid = 3
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
            
        usuario = request.user
        saludo = saludo_dia()
            
        rol = get_object_or_404(Roles, id=rol_id)
        pr = rol.permisos.all()
        rol.estado = False
        rol.save()
            
        return render_to_response('roles/gracias.html', {'aid':aid, 'usuario':usuario, 'saludo':saludo, 'rol':rol, 'pr':pr})  
    else:
        return HttpResponseRedirect('/index')
    
def index_roles(request):
    """
    Método que nos permite conocer los tipos de roles con la cual cuenta un usuario.

    @param request:Http request
    @type  request:HtpptRequest 
    @return: render a roles/index.html.
    
    """    
    
    usuario = request.user
    accion = "Index de Roles"
    
    staff = verificar_permiso(usuario, accion)
    
    if staff:
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
            
        saludo = saludo_dia()
        rolex = Roles.objects.all().exclude(nombre="Administrador")
        roles = Roles.objects.order_by('id').exclude(nombre="Administrador")
        for r in roles:
            rol_usuario = Roles_Usuarios_Proyectos.objects.filter(roles=r)
            if rol_usuario:
                rolex= rolex.exclude(id=r.id)
        filas= roles.count()

            
        if request.method == 'POST':
            results = Roles.objects.all()
            form = BuscarRolForm(request.POST)
                
            if form.is_valid():
                rid = request.POST.get('id', None)
                if rid:
                    results = results.filter(id=rid)
                    
                rnombre = request.POST.get('nombre', None)
                if rnombre:
                    results = results.filter(nombre__icontains=rnombre)
                    
                robservacion = request.POST.get('observacion', None)
                if robservacion:
                    results = results.filter(observacion__icontains=robservacion)
                            
                if not rid and not rnombre and not robservacion:
                    results = None
                    
                if results:
                    results.order_by('id')
                return render_to_response('roles/results.html', {'usuario':usuario, 'saludo':saludo, 'results':results}, context_instance=RequestContext(request))
        else:
            form = BuscarRolForm()
            
        return render(request, 'roles/index.html', {'usuario':usuario, 'saludo':saludo, 'rolex':rolex, 'roles':roles, 'filas':filas})
    else:
        return HttpResponseRedirect('/index')


"""Administración de Proyectos"""
def crear_proyectos(request):
    """
    Metodo que crea un Nuevo proyecto en el sistema
    
    @param request: Http request
    @type  request:HtpptRequest 
    @return: render al template proyectos/gracias.html
    """
    usuario = request.user
    accion = "Registro de Proyectos/Servicios"
    
    staff = verificar_permiso(usuario, accion)
    
    if staff:
        aid = 1
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
            
        saludo = saludo_dia()
        
        rol = get_object_or_404(Roles, nombre="Scrum Master")
        usuarios = User.objects.all().exclude(id=1)
        
        if request.method == 'POST':
            form = CrearProyectoForm(request.POST, request.FILES)
            
            if form.is_valid():
                cleaned_data = form.cleaned_data
                nombre_largo = cleaned_data.get('nombre_largo')
                user_id = cleaned_data.get('user_id')
            
                proyecto = Proyectos()
                proyecto.nombre_largo = nombre_largo
                proyecto.estado = 1
                proyecto.save()
                
                user_profile = Usuarios.objects.get(id=user_id)
                  
                up = Usuarios_Proyectos(proyecto=proyecto, usuarios=user_profile)
                up.save()
                  
                rup = Roles_Usuarios_Proyectos(roles=rol, proyecto=proyecto, usuarios=user_profile)
                rup.save()
                
                    
                return render_to_response('proyectos/gracias.html', {'aid':aid, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto}, context_instance=RequestContext(request))
        
        else:
            form = CrearProyectoForm()
            
        return render(request, 'proyectos/crear.html', {'usuarios':usuarios, 'rol':rol, 'usuario':usuario, 'saludo':saludo, 'form': form})
    else:
        return HttpResponseRedirect('/index')
    
def definir_proyectos(request, user_id, proyecto_id):
    """
    Metodo que define los parametros de un proyecto
    
    @param request: Http request
    @type  request:HtpptRequest 
    @param request: proyecto_id
    @return: render al template proyectos/gracias.html
    
    """
    
    usuario = User.objects.get(id=user_id)
    accion = "Definir Proyectos/Servicios"
    
    staff = verificar_permiso(usuario, accion)
    
    if staff:
        aid = 2
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
             
        saludo = saludo_dia()
            
        proyecto = get_object_or_404(Proyectos, id=proyecto_id)
   
        if request.method == 'POST':
            form = DefinirProyectoForm(request.POST, request.FILES)
            
            if form.is_valid():
                cleaned_data = form.cleaned_data
                nombre_corto = cleaned_data.get('nombre_corto')
                tipo = cleaned_data.get('tipo')
                estado = cleaned_data.get('estado')
                descripcion = cleaned_data.get('descripcion')
                fecha_inicio = cleaned_data.get('fecha_inicio')
                fecha_fin_estimado = cleaned_data.get('fecha_fin_estimado')
            
                proyecto.nombre_corto = nombre_corto
                proyecto.tipo = tipo
                proyecto.descripcion = descripcion
                proyecto.fecha_inicio = fecha_inicio
                proyecto.fecha_fin_estimado = fecha_fin_estimado
                proyecto.estado = estado
                proyecto.save()

                return render_to_response('proyecto_usuario/gracias.html', {'staff':staff, 'aid':aid, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto}, context_instance=RequestContext(request))
        
        else:
            form = DefinirProyectoForm()
            
        return render(request, 'proyecto_usuario/definir.html', {'staff':staff, 'proyecto':proyecto, 'usuario':usuario, 'saludo':saludo, 'form': form})
    else:
        return HttpResponseRedirect('/index')

def editar_proyectos(request, proyecto_id):
    """
    Metodo que edita los parametros de un proyecto
    
    @param request: Http request
    @type  request:HtpptRequest 
    @param request: proyecto_id
    @return: render al template proyectos/gracias.html
    
    """
    
    usuario = request.user
    accion = "Editar Proyectos/Servicios"
    
    staff = verificar_permiso(usuario, accion)
    
    if staff:
        aid = 3
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
            
        saludo = saludo_dia()
            
        proyecto = get_object_or_404(Proyectos, id=proyecto_id)
        rol = get_object_or_404(Roles, nombre="Scrum Master")
        sm = proyecto.usuarios.get(roles=rol)
        lista = proyecto.usuarios.all().exclude(id=sm.id)
        
        if request.method == 'POST':
            form = EditarProyectoForm(request.POST, request.FILES)
            
            if form.is_valid():
                cleaned_data = form.cleaned_data
                observaciones = cleaned_data.get('observaciones')
                user_id = cleaned_data.get('user_id')
                
                proyecto.observaciones = observaciones
                proyecto.save()
                
                if user_id:
                    desasignar_usuarios(request, sm.id, proyecto_id)
                    user_profile = Usuarios.objects.get(id=user_id)
                    desasignar_usuarios(request, user_profile.id, proyecto_id)
                    
                    up = Usuarios_Proyectos(proyecto=proyecto, usuarios=user_profile)
                    up.save()
                      
                    rup = Roles_Usuarios_Proyectos(roles=rol, proyecto=proyecto, usuarios=user_profile)
                    rup.save()
                
                usuarios = proyecto.usuarios.all()
                            
                return render_to_response('proyectos/gracias.html', {'aid':aid, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto, 'usuarios':usuarios}, context_instance=RequestContext(request))
        
        else:
            form = EditarProyectoForm()
        return render(request, 'proyectos/editar.html', {'rol':rol, 'sm':sm, 'lista':lista, 'usuario':usuario, 'saludo':saludo, 'form': form, 'proyecto':proyecto})
    else:
        return HttpResponseRedirect('/index')

def desasignar_usuarios(request, user_id, proyecto_id):
    """
    Método para desasignar a un usuario existente del proyecto.
    
    @param request: Http request
    @type  request:HtpptRequest 
    @param request: proyecto_id
    @return: se eliminaron los registros que relacionan al usuario con el proyecto, con el rol. 
    
    """
    
    proyecto = get_object_or_404(Proyectos, id=proyecto_id)
    
    usuario = get_object_or_404(Usuarios, id=user_id)
    us_pr = get_object_or_404(Usuarios_Proyectos, proyecto=proyecto, usuarios=usuario)
    rol_us_pr = get_object_or_404(Roles_Usuarios_Proyectos, proyecto=proyecto, usuarios=usuario)
            
    rol_us_pr.delete()
    us_pr.delete()
    

def ver_proyectos(request, proyecto_id):
    """
    Metodo que permite visualizar el proyecto seleccionado
    
    @param request: Http request
    @type  request:HtpptRequest 
    @param request: proyecto_id
    @return: render al template proyectos/ver.html
    """
    usuario = request.user
    accion = "Ver Proyectos/Servicios"
    
    staff = verificar_permiso(usuario, accion)
    
    roles=[]
    
    if staff:
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
            
        saludo = saludo_dia()
            
        proyecto = get_object_or_404(Proyectos, id=proyecto_id)
        up = proyecto.usuarios.all()
        for u in up:
            rol = get_object_or_404(Roles_Usuarios_Proyectos, proyecto=proyecto, usuarios=u)
            r= get_object_or_404(Roles, nombre=rol.roles.nombre)
            roles.append(r)
        ur = map(None, up, roles)
        
        return render(request, 'proyectos/ver.html', {'ur':ur, 'up':up, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto})
    else:
        return HttpResponseRedirect('/index')
    
def index_proyectos(request):
    """
    Metodo que permite visualizar proyectos
    
    @param request: Http request
    @type  request:HtpptRequest 
    @return: render al template proyectos/results.html
    """
    usuario = request.user
    accion = "Index de Proyectos/Servicios"
    
    staff = verificar_permiso(usuario, accion)
    
    if staff:
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
            
        saludo = saludo_dia()
            
        proyectos = Proyectos.objects.all().order_by('id')
        filas= proyectos.count()
            
        if request.method == 'POST':
            results = Proyectos.objects.all()
            form = BuscarProyectoForm(request.POST)
                
            if form.is_valid():
                pid = request.POST.get('id', None)
                if pid:
                    results = results.filter(id=pid)
                    
                pnombre_largo = request.POST.get('nombre_largo', None)
                if pnombre_largo:
                    results = results.filter(nombre_largo__icontains=pnombre_largo)
                    
                pnombre_corto = request.POST.get('nombre_corto', None)
                if pnombre_corto:
                    results = results.filter(nombre_corto__icontains=pnombre_corto)
                    
                pdescripcion = request.POST.get('descripcion', None)
                if pdescripcion:
                    results = results.filter(descripcion_icontains=pdescripcion)
                            
                if not pid and not pnombre_corto and not pnombre_largo and not pdescripcion:
                    results = None
                    
                if results:
                    results.order_by('id')
                return render_to_response('proyectos/results.html', {'usuario':usuario, 'saludo':saludo, 'results':results}, context_instance=RequestContext(request))
        else:
            form = BuscarProyectoForm()
            
        return render(request, 'proyectos/index.html', {'usuario':usuario, 'saludo':saludo, 'proyectos':proyectos, 'filas':filas})
    else:
        return HttpResponseRedirect('/index')


def index_ususario_proyecto(request, user_id, proyecto_id):
    """
    Método que muestra la página de inicio de un Usuario no administrador, en un Proyecto seleccionado.
    
    @param request: Http request
    @type  request:HtpptRequest 
    @param user_id: Id de un usuario registrado en el sistema.
    @param proyecto_id: Id de un proyecto registrado en el sistema.
    @return: render al template inicio_usuario.html cuando accede a un proyecto seleccionado.
    
    """
    
    comprobar(request)
    if(request.user.is_anonymous()):
        return HttpResponseRedirect('/ingresar')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['last_activity'] = str(now)
    user = request.user
    accion = "Definir Proyectos/Servicios"
    staff = verificar_permiso(user, accion)  
        
    saludo = saludo_dia()
    usuario = User.objects.get(id=user_id)
    proyecto = Proyectos.objects.get(id=proyecto_id)

    return render_to_response('inicio_usuario.html', {'staff':staff, 'usuario':usuario, 'proyecto':proyecto, 'saludo':saludo}, context_instance=RequestContext(request)) 

def index_proyecto_usuario(request, user_id, proyecto_id):
    """
    Método que muestra la página de inicio de Proyecto de un Usuario, en un Proyecto seleccionado.
    Si es Scrum Master, muesta la lista de Usuarios y User Stories asignados al Proyecto.
    Si es Usuario Regular, muestra la lista de User Stories.
    
    @param request: Http request
    @type  request:HtpptRequest 
    @param user_id: Id de un usuario registrado en el sistema.
    @param proyecto_id: Id de un proyecto registrado en el sistema.
    @return: render al template proyecto_usuario/index.html para ver página de inicio de proyecto. 
             render al template proyecto_usiario/results.html para obtener resultado de búsqueda.
    
    """
    
    user = request.user
    accion = "Definir Proyectos/Servicios"
    accion2 = "Listar US"
    
    staff = verificar_permiso(user, accion)
    staff2 = verificar_permiso(user, accion2)
    
    comprobar(request)
    if(request.user.is_anonymous()):
        return HttpResponseRedirect('/ingresar')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['last_activity'] = str(now)
            
    saludo = saludo_dia()
    usuario = Usuarios.objects.get(id=user_id)
    proyecto = Proyectos.objects.get(id=proyecto_id)
            
    rup = get_object_or_404(Roles_Usuarios_Proyectos, proyecto=proyecto, usuarios=usuario)
    rol = get_object_or_404(Roles, nombre=rup.roles.nombre)
    usuarios = proyecto.usuarios.all().exclude(id=user.id).exclude(user__is_active=False)
    filas = usuarios.count()
    uh = proyecto.user_stories.all().order_by('id')
    filax = uh.count()
    
    lista_roles = []
    lista_usuarios = []
    for u in usuarios:
        r = get_object_or_404(Roles_Usuarios_Proyectos, proyecto=proyecto, usuarios=u)
        lista_roles.append(r.roles)
        lista_usuarios.append(u)
    
    pr = map(None, lista_usuarios, lista_roles)
    
    if staff:    
        if request.method == 'POST':
            results = proyecto.usuarios.all().exclude(id=usuario.id)
            form = BuscarUserForm(request.POST)
                
            if form.is_valid():
                uid = request.POST.get('id', None)
                if uid:
                    if uid != usuario.user.id:
                        results = results.filter(id__iexact=uid)
                    else:
                        results = None
                            
                uusername = request.POST.get('username', None)
                if uusername:
                    if uusername != usuario.user.username:
                        results = results.filter(user__username__icontains=uusername)
                    else:
                        results = None
                            
                uemail = request.POST.get('email', None)
                if uemail:
                    if uemail != usuario.user.email:
                        results = results.filter(user__uemail__icontains=uemail)
                    else:
                        results = None
                            
                first_name = request.POST.get('first_name', None)
                if first_name:
                    if first_name != usuario.user.first_name:
                        results = results.filter(user__first_name__icontains=first_name)
                    else:
                        results = None
                            
                last_name = request.POST.get('last_name', None)
                if last_name:
                    if last_name != usuario.user.last_name:
                        results = results.filter(user__last_name__icontains=last_name)
                    else:
                        results = None
                            
                if not uid and not uusername and not uemail and not first_name and not last_name:
                    results = None
                    
                if results:
                    results.order_by('id')
                return render_to_response('proyecto_usuario/results.html', {'user':user, 'proyecto':proyecto, 'saludo':saludo, 'results':results}, context_instance=RequestContext(request))
        else:
            form = BuscarUserForm()
    if staff or staff2:
        us_us1 = User_Story.objects.filter(usuario_asignado=usuario)
        us_us = None
        activo = 1
        if us_us1:
            us_us = User_Story.objects.get(usuario_asignado=usuario)
        
            us_sp1 = US_Sprint.objects.filter(user_story=us_us)
            if us_sp1:
                us_sp = US_Sprint.objects.get(user_story=us_us)
                if us_sp:
                    activo = us_sp.sprint.estado
                else:
                    activo = 1
            
        if request.method == 'POST':
            results = proyecto.usuarios.all().exclude(id=usuario.id)
            form = BuscarUSForm(request.POST)
                
            if form.is_valid():
                usid = request.POST.get('id', None)
                if usid:
                    results = results.filter(id__iexact=usid)
                            
                usnombre = request.POST.get('nombre', None)
                if usnombre:
                    results = results.filter(nombre__icontains=usnombre)
                            
                usdescripcion = request.POST.get('descripcion', None)
                if usdescripcion:
                    results = results.filter(descripcion__icontains=usdescripcion)

                if not usid and not usnombre and not usdescripcion:
                    results = None
                    
                if results:
                    results.order_by('id')
                return render_to_response('proyecto_usuario/results.html', {'user':user, 'proyecto':proyecto, 'saludo':saludo, 'results':results}, context_instance=RequestContext(request))
        else:
            form = BuscarUSForm()
        return render_to_response('proyecto_usuario/index.html', {'pr':pr, 'activo':activo, 'us_us':us_us, 'filax':filax, 'uh':uh, 'filas':filas, 'staff2':staff2, 'staff':staff, 'usuarios':usuarios, 'rol':rol, 'user':user, 'proyecto':proyecto, 'saludo':saludo}, context_instance=RequestContext(request)) 
    else:
        return HttpResponseRedirect('/index')
    
def eliminar_usuario_proyecto(request, user_id, userd_id, proyecto_id):
    """
    Método que permite desasignar un Usuario de un Proyecto, así como también el Rol asociado al Usuario.
    
    @param request: Http request
    @type  request:HtpptRequest 
    @param user_id: Id de un usuario registrado en el sistema, que realiza la acción (Scrum Master).
    @param userd_id: Id de un usuario registrado en el sistema, que es objeto de la acción (Usuario Regular).
    @return: render al template proyecto_usuario/gracias.html cuando se ha desasignado correctamente.
             Usuario desasignado del Proyecto.
             Rol desasignado del Usuario.
    """
    user = request.user
    accion = "Definir Proyectos/Servicios"
    staff = verificar_permiso(user, accion)
    
    if staff:
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
        aid = 2   
        saludo = saludo_dia()
        usuario = Usuarios.objects.get(id=userd_id)
        proyecto = Proyectos.objects.get(id=proyecto_id)
        desasignar_usuarios(request, usuario.id, proyecto.id)
    else:
        return HttpResponseRedirect('/index')
    
    return render_to_response('proyecto_usuario/gracias.html', {'aid':aid, 'user':user, 'saludo':saludo, 'proyecto':proyecto}, context_instance=RequestContext(request))

def asignar_roles_usuarios_proyecto(request, user_id, proyecto_id):
    """
    Método que permite asignar un Rol a un Usuario en un Proyecto determinado.
    
    @param request: Http request
    @type  request:HtpptRequest 
    @param user_id: Id de un usuario registrado en el sistema.
    @return: render al template usuarios/asignar.html para la asignación. 
             render al template usuarios/gracias.html cuando se ha asignado correctamente.
    """
    
    usuario = request.user
    proyecto = Proyectos.objects.get(id=proyecto_id)
    accion = "Asginar Rol a Usuarios en un Proyecto"
    
    staff = verificar_permiso(usuario, accion)
    
    if staff:
        aid = 2
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
        
        saludo = saludo_dia()
        
        roles = Roles.objects.filter(estado=True).exclude(nombre="Administrador").exclude(nombre="Scrum Master")
        usuarios = Usuarios.objects.all().exclude(id=user_id).exclude(user__is_active=False).exclude(id=1)
        usuariox = proyecto.usuarios.all()
        
        if request.method == 'POST':
            form = AsignarRolForm(request.POST)
            if form.is_valid():
                rol_id = request.POST.get('rol_id', None)
                userd_id = request.POST.get('userd_id', None)
                   
                rol = get_object_or_404(Roles, id=rol_id) 
                proyecto = get_object_or_404(Proyectos, id=proyecto_id)
                user_profile = get_object_or_404(Usuarios, id=userd_id)
                    
                up = Usuarios_Proyectos(proyecto=proyecto, usuarios=user_profile)
                up.save()
                 
                rup = Roles_Usuarios_Proyectos(roles=rol, proyecto=proyecto, usuarios=user_profile)
                rup.save()
                 
                return render_to_response('proyecto_usuario/gracias.html', {'staff':staff, 'aid':aid, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto, 'r':rol}, context_instance=RequestContext(request))
        else:
            form = AsignarRolForm()
        return render(request, 'proyecto_usuario/asignar.html', {'staff':staff, 'form': form, 'roles':roles, 'usuariox':usuariox, 'usuarios':usuarios, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto})
    else:
        return HttpResponseRedirect('/index')

"Gestión de US"
def crear_us(request, user_id, proyecto_id):
    """
    Método que permite crear un User Story en un Proyecto determinado.
    
    @param request: Http request
    @type  request:HtpptRequest 
    @param user_id: Id de un usuario registrado en el sistema.
    @param proyecto_id: Id de un proyecto registrado en el sistema.
    @return: render al template user_history/crear.html para la cración. 
             render al template user_history/gracias.html cuando se ha creado correctamente.
             User Story creado.
    """
    
    usuario = request.user
    proyecto = Proyectos.objects.get(id=proyecto_id)
    accion = "Crear US"
    accion1 = "Desarrollar US"
    accion2 = "Crear Tipo"
    accion3 = "Definir Prioridad SM"
    staff = verificar_permiso(usuario, accion)
    staff1 = verificar_permiso(usuario, accion1)
    staff2 = verificar_permiso(usuario, accion2)
    staff3 = verificar_permiso(usuario, accion3)
    
    tipos = Tipo.objects.all()
    
    if staff or staff1 or staff2:
        aid = 1
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
        
        saludo = saludo_dia()
        if request.method == 'POST':
            form = CrearUSForm(request.POST, proyecto_id=proyecto_id)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                nombre = cleaned_data.get('nombre')
                descripcion = cleaned_data.get('descripcion')
                prioridad_SM = cleaned_data.get('prioridad_SM')
                nivel_prioridad = cleaned_data.get('nivel_prioridad')
                valor_negocios = cleaned_data.get('valor_negocios')
                valor_tecnico = cleaned_data.get('valor_tecnico')
                size = cleaned_data.get('size')
                tiempo_estimado = cleaned_data.get('tiempo_estimado')
                tipo_creado = cleaned_data.get('tipo_creado')
                tipo = cleaned_data.get('tipo')
                
                if tipo_creado:
                    atype = Tipo(nombre=tipo_creado)
                    atype.save()
                else:
                    atype = Tipo.objects.get(nombre=tipo)
                
                us = User_Story()
                us.nombre = nombre
                us.descripcion = descripcion
                if staff3:
                    us.prioridad_SM = prioridad_SM
                us.nivel_prioridad = nivel_prioridad
                us.valor_negocios = valor_negocios
                us.valor_tecnico = valor_tecnico
                us.size = size
                us.tiempo_estimado = tiempo_estimado
                us.fecha_creacion = datetime.now()
                us.tipo = atype
                us.save()
                
                us_p = US_Proyectos(proyecto=proyecto, user_story=us)
                us_p.save()
                
                if staff2:
                    if tipo_creado: 
                        flujo = Flujos()
                    else:
                        flujo = Flujos.objects.get(tipo=atype)
                    flujo.nombre = atype.nombre
                    flujo.tipo = atype
                    flujo.save()
                    
                    if tipo_creado: 
                        f_p = Flujos_Proyectos(proyecto=proyecto, flujo=flujo)
                        f_p.save()
                
                return render_to_response('user_history/gracias.html', {'staff':staff, 'us':us, 'aid':aid, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto}, context_instance=RequestContext(request))
        else:
            form = CrearUSForm(proyecto_id=proyecto_id)
        return render(request, 'user_history/crear.html', {'tipos':tipos, 'staff3':staff3, 'staff2':staff2, 'staff':staff, 'form': form, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto})
    else:
        return HttpResponseRedirect('/index')
    
def modificar_us(request, us_id, user_id, proyecto_id):
    """
    Método que permite modificar un User Story seleccionado en un Proyecto determinado.
    
    @param request: Http request
    @type  request:HtpptRequest 
    @param us_id: Id de un user story registrado en el sistema.
    @param user_id: Id de un usuario registrado en el sistema.
    @param proyecto_id: Id de un proyecto registrado en el sistema.
    @return: render al template user_history/modificar.html para la modificación. 
             render al template user_history/gracias.html cuando se ha modificado correctamente.
             User Story modificado.
    """
    
    usuario = request.user
    proyecto = Proyectos.objects.get(id=proyecto_id)
    
    accion = "Crear US"
    accion1 = "Modificar US - ValNeg"
    accion2 = "Modificar US - ValTec"
    accion3 = "Modificar US - Size"         
    accion4 = "Modificar US - Prioridad"
    accion5 = "Modificar US - Notas"
    accion6 = "Modificar US - ArchAdj"
    accion7 = "Modificar US - Descripción"
    accion8 = "Definir Prioridad SM"
    accion9 = "Modificar US - TEst"
    accion10 = "Modificar US - Desarrollador"

    staff = verificar_permiso(usuario, accion)
    staff1 = verificar_permiso(usuario, accion1)
    staff2 = verificar_permiso(usuario, accion2)
    staff3 = verificar_permiso(usuario, accion3)
    staff4 = verificar_permiso(usuario, accion4)
    staff5 = verificar_permiso(usuario, accion5)
    staff6 = verificar_permiso(usuario, accion6)
    staff7 = verificar_permiso(usuario, accion7)
    staff8 = verificar_permiso(usuario, accion8)    
    staff9 = verificar_permiso(usuario, accion9)
    staff10 = verificar_permiso(usuario, accion10)
    
    us = proyecto.user_stories.get(id=us_id)
    if staff1 or staff2 or staff3 or staff4 or staff5 or staff6 or staff7 or staff9 or staff10:
        aid = 2
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
        
        saludo = saludo_dia()
        list_usuarios_asginados = []
        usuarios = proyecto.usuarios.all()
        
        if request.method == 'POST':
            form = EditarUSForm(request.POST)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                descripcion = cleaned_data.get('descripcion')
                prioridad_SM = cleaned_data.get('prioridad_SM')
                nivel_prioridad = cleaned_data.get('nivel_prioridad')
                valor_negocios = cleaned_data.get('valor_negocios')
                valor_tecnico = cleaned_data.get('valor_tecnico')
                size = cleaned_data.get('size')
                tiempo_estimado = cleaned_data.get('tiempo_estimado')
                id_user = cleaned_data.get('id_user')
                
                if staff7:
                    us.descripcion = descripcion
                if staff4:
                    us.nivel_prioridad = nivel_prioridad
                if staff1:
                    us.valor_negocios = valor_negocios
                if staff2:
                    us.valor_tecnico = valor_tecnico
                if staff3:
                    us.size = size
                if staff8:
                    us.prioridad_SM = prioridad_SM
                if staff9:
                    us.tiempo_estimado = tiempo_estimado
                
                if staff10:
                    userstories = proyecto.user_stories.all()
    
                    for uh in userstories:
                        list_usuarios_asginados.append(uh.usuario_asignado)

                    usuarios = usuarios.filter(roles__permisos__nombre="Desarrollo de US")
                    
                    if id_user:
                        usuario_asignado = Usuarios.objects.get(id=id_user)
                        us.usuario_asignado = usuario_asignado
                        
                us.save()
                
                return render_to_response('user_history/gracias.html', {'us':us, 'aid':aid, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto, 'staff':staff}, context_instance=RequestContext(request))
        else:
            form = EditarUSForm()
        return render(request, 'user_history/modificar.html', {'form': form, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto, 'us':us, 'staff1':staff1, 'staff':staff,\
                                                               'staff2':staff2, 'staff3':staff3, 'staff4':staff4, 'staff5':staff5, 'staff6':staff6, 'staff7':staff7, 'staff8':staff8,\
                                                               'staff9':staff9, 'staff10':staff10, 'list_usuarios_asginados':list_usuarios_asginados, 'usuarios':usuarios,})
    else:
        return HttpResponseRedirect('/index')

def asignar_us(request, user_id, proyecto_id, us_id):
    """
    Método que permite asignar un User Story a un Usuario en un Proyecto determinado.
    
    @param request: Http request
    @type  request:HtpptRequest 
    @param us_id: Id de un user story registrado en el sistema.
    @param user_id: Id de un usuario registrado en el sistema.
    @param proyecto_id: Id de un proyecto registrado en el sistema.
    @return: render al template user_history/asginar.html para la asignación. 
             render al template user_history/gracias.html cuando se ha asignado correctamente.
             User Story asignado a un Usuario.
    """
    usuario = request.user
    proyecto = Proyectos.objects.get(id=proyecto_id)

    accion = "Asignar US"
    staff = verificar_permiso(usuario, accion)
    
    us = proyecto.user_stories.get(id=us_id)
    sp = Sprint.objects.get(id=us.id_sprint)
    
    userstories = proyecto.user_stories.all()
    list_usuarios_asginados = []
    
    for uh in userstories:
        list_usuarios_asginados.append(uh.usuario_asignado)

    usuarios = sp.desarrolladores.all()
    usuarios = usuarios.filter(roles__permisos__nombre="Desarrollo de US").filter(asignado=False)

    if staff:
        aid = 3
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
        
        saludo = saludo_dia()
        if request.method == 'POST':
            form = AsignarUSForm(request.POST)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                id_user = cleaned_data.get('id_user')
                
                usuario_asignado = Usuarios.objects.get(id=id_user)
                
                if not us.usuario_asignado:
                    us.usuario_asignado = usuario_asignado
                    us.save()
                else:
                    ussp = Usuarios_Sprint.objects.get(desarrolladores=usuario_asignado, sprint=sp)
                    ussp.delete()
                    
                    us.usuario_asignado.asignado = False
                    us.usuario_asignado = usuario_asignado
                    us.save()

                if not usuario_asignado.asignado:
                    duracion = us.tiempo_estimado/usuario_asignado.horas_por_dia.cantidad_diaria
                    duracion = math.ceil(duracion)
                    if duracion > sp.duracion:
                        sp.duracion = duracion      
                        sp.save()
                
                usuario_asignado.asignado = True
                usuario_asignado.save()
                
                ussp = Usuarios_Sprint.objects.get(desarrolladores=usuario_asignado, sprint=sp)
                if not ussp.user_story:
                    ussp.user_story = us
                    ussp.save()
                else:
                    ussp = Usuarios_Sprint(desarrolladores=usuario_asignado, sprint=sp, user_story=us)
                
                return render_to_response('user_history/gracias.html', {'staff':staff, 'us':us, 'aid':aid, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto}, context_instance=RequestContext(request))
        else:
            form = AsignarUSForm()
        return render(request, 'user_history/asignar.html', {'form': form, 'list_usuarios_asginados':list_usuarios_asginados, 'usuarios':usuarios, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto, 'us':us, 'staff':staff})
    else:
        return HttpResponseRedirect('/index')


def date_by_adding_business_days(from_date, add_days):
    business_days_to_add = add_days
    current_date = from_date
    while business_days_to_add > 0:
        current_date += timedelta(days=1)
        weekday = current_date.weekday()
        if weekday >= 5: # sunday = 6
            continue
        business_days_to_add -= 1
    return current_date

def reportar_avance_us(request, user_id, proyecto_id, us_id):
   
    user = request.user
    accion = "Desarrollar US"
    
    staff = verificar_permiso(user, accion)
    
    if staff:
        aid = 5
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
                
        saludo = saludo_dia()
        
        usuario = Usuarios.objects.get(id=user_id)
        proyecto = Proyectos.objects.get(id=proyecto_id)
        us = User_Story.objects.get(id=us_id)
    
        if request.method == 'POST':
            form = ReportarUSForm(request.POST)
                
            if form.is_valid():
                cleaned_data = form.cleaned_data
                descripcion = cleaned_data.get('descripcion')
                horas_faltantes = cleaned_data.get('horas_faltantes')
                porcentaje_alcanzado = cleaned_data.get('porcentaje_alcanzado')
                
                reporte = Reporte()
                reporte.descripcion = descripcion
                reporte.horas_faltantes = horas_faltantes
                reporte.porcentaje_alcanzado = porcentaje_alcanzado
                reporte.fecha_reporte = datetime.now()
                reporte.save()

                us_reporte = US_Reportes(user_story=us, reporte=reporte)
                us_reporte.save()
                                
                return render_to_response('user_history/gracias.html', {'reporte':reporte, 'us':us, 'aid':aid, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto, 'staff':staff}, context_instance=RequestContext(request))
        else:
            form = ReportarUSForm()
        return render_to_response('user_history/reportar_avance.html', {'staff':staff, 'us':us, 'user':user, 'proyecto':proyecto, 'saludo':saludo}, context_instance=RequestContext(request)) 
    else:
        return HttpResponseRedirect('/index')

def ver_reporte_us(request, user_id, proyecto_id, us_id):
    usuario = request.user
    proyecto = Proyectos.objects.get(id=proyecto_id)

    accion = "Visualizar US"
   
    staff = verificar_permiso(usuario, accion)
    
    us = proyecto.user_stories.get(id=us_id)
        
    if staff:
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
        
        saludo = saludo_dia()
        reportes = us.reportes.all()
        
        return render(request, 'user_history/ver_reportes.html', {'reportes':reportes, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto, 'us':us})
    else:
        return HttpResponseRedirect('/index')
    
def index_us(request, user_id, proyecto_id):
    """
    Método de inicio que permite ver los User Stories de un Proyecto determinado, así como también la búsqueda de los mismos.
    
    @param request: Http request
    @type  request:HtpptRequest 
    @param user_id: Id de un usuario registrado en el sistema.
    @param proyecto_id: Id de un proyecto registrado en el sistema.
    @return: render al template user_history/index.html para la página de inicio.
             render al template user_history/results.html para obtener resultados de la búsqueda.  
             Listado de US.
    """
    user = request.user
    accion = "Listar US"
    
    staff = verificar_permiso(user, accion)
    
    if staff:
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
                
        saludo = saludo_dia()
        usuario = Usuarios.objects.get(id=user_id)
        proyecto = Proyectos.objects.get(id=proyecto_id)
                
        uh = proyecto.user_stories.all().order_by('id')
        filax = uh.count()
    
        if request.method == 'POST':
            results = proyecto.user_stories.all().exclude(id=usuario.id)
            form = BuscarUSForm(request.POST)
                
            if form.is_valid():
                usid = request.POST.get('id', None)
                if usid:
                    results = results.filter(id__iexact=usid)
                            
                usnombre = request.POST.get('nombre', None)
                if usnombre:
                    results = results.filter(nombre__icontains=usnombre)
                            
                usdescripcion = request.POST.get('descripcion', None)
                if usdescripcion:
                    results = results.filter(descripcion__icontains=usdescripcion)

                if not usid and not usnombre and not usdescripcion:
                    results = None
                    
                if results:
                    results.order_by('id')
                return render_to_response('user_history/results.html', {'user':user, 'proyecto':proyecto, 'saludo':saludo, 'results':results}, context_instance=RequestContext(request))
        else:
            form = BuscarUSForm()
        return render_to_response('user_history/index.html', {'filax':filax, 'uh':uh, 'staff':staff, 'user':user, 'proyecto':proyecto, 'saludo':saludo}, context_instance=RequestContext(request)) 
    else:
        return HttpResponseRedirect('/index')

def ver_us(request, user_id, proyecto_id, us_id):
    """
    Método que nos permite ver los user stories de un proyecto especifico.
    
    @param request: Http request
    @type  request:HtpptRequest 
    @param user_id: Id de un usuario registrado en el sistema.
    @param proyecto_id: Id de un proyecto registrado en el sistema.
    @return: render al template user_history/ver.html.
             
    """
    
    usuario = request.user
    proyecto = Proyectos.objects.get(id=proyecto_id)

    accion = "Visualizar US"
   
    staff = verificar_permiso(usuario, accion)
    
    us = proyecto.user_stories.get(id=us_id)
        
    if staff:
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
        
        saludo = saludo_dia()
        
        return render(request, 'user_history/ver.html', {'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto, 'us':us})
    else:
        return HttpResponseRedirect('/index')

def cambiar_estado_us(request, user_id, proyecto_id, us_id):
    """
    Método que nos permite cambiar el estado de un user story especifico.
    
    @param request: Http request
    @type  request:HtpptRequest 
    @param user_id: Id de un usuario registrado en el sistema.
    @param proyecto_id: Id de un proyecto registrado en el sistema.
    @return: render al template user_history/cambiar_estado.html.
             
    """

    usuario = request.user
    proyecto = Proyectos.objects.get(id=proyecto_id)

    accion = "Crear US"
    accion1 = "Cambiar estado US"
    staff = verificar_permiso(usuario, accion)
    staff1 = verificar_permiso(usuario, accion1)
    us = proyecto.user_stories.get(id=us_id)
    sp = proyecto.sprint.get(id=us.id_sprint)
        
    if staff or staff1:
        aid = 4
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
        
        saludo = saludo_dia()
        
        cambio_estado = True
        if sp.estado == 2:
            cambio_estado = False
            
        if request.method == 'POST':
            form = CambiarEstadoUSForm(request.POST)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                estado = cleaned_data.get('estado')
                tiempo_real = cleaned_data.get('tiempo_real')
                
                if estado:
                    us.estado = estado
                    if estado == 3:
                        if tiempo_real:
                            us.tiempo_real = tiempo_real
                us.save()
                
                if tiempo_real > (sp.duracion*8):
                    us_sp = US_Sprint.objects.get(user_story=us, sprint=sp)
                    us_sp.delete()
                    
                    us.id_sprint = None
                    us.tiempo_real = tiempo_real
                    us.estado = 4
                    us.reestimar = True
                    us.save()
                
                return render_to_response('user_history/gracias.html', {'staff':staff, 'us':us, 'aid':aid, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto}, context_instance=RequestContext(request))
        else:
            form = CambiarEstadoUSForm()
        return render(request, 'user_history/cambiar_estado.html', {'cambio_estado':cambio_estado, 'staff':staff, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto, 'us':us})
    else:
        return HttpResponseRedirect('/index')
    
def notas_us(request, user_id, proyecto_id, us_id): 
    user = request.user
    accion = "Notas US"
    
    staff = verificar_permiso(user, accion)
    
    if staff:
        aid = 6
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
                
        saludo = saludo_dia()
        
        usuario = Usuarios.objects.get(id=user_id)
        proyecto = Proyectos.objects.get(id=proyecto_id)
        us = User_Story.objects.get(id=us_id)
    
        if request.method == 'POST':
            form = NotasUSForm(request.POST)
                
            if form.is_valid():
                cleaned_data = form.cleaned_data
                nombre = cleaned_data.get('nombre')
                descripcion = cleaned_data.get('descripcion')

                nota = Nota()
                nota.nombre = nombre
                nota.descripcion = descripcion
                nota.usuario = usuario
                nota.save()

                us_nota = US_Notas(user_story=us, nota=nota)
                us_nota.save()
                                
                return render_to_response('user_history/gracias.html', {'nota':nota, 'us':us, 'aid':aid, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto, 'staff':staff}, context_instance=RequestContext(request))
        else:
            form = NotasUSForm()
        return render_to_response('user_history/agregar_notas.html', {'staff':staff, 'us':us, 'user':user, 'proyecto':proyecto, 'saludo':saludo}, context_instance=RequestContext(request)) 
    else:
        return HttpResponseRedirect('/index')
    
def ver_notas_us(request, user_id, proyecto_id, us_id):
    usuario = request.user
    proyecto = Proyectos.objects.get(id=proyecto_id)

    accion = "Visualizar US"
   
    staff = verificar_permiso(usuario, accion)
    
    us = proyecto.user_stories.get(id=us_id)
        
    if staff:
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
        
        saludo = saludo_dia()
        notas = us.notas.all()
        
        return render(request, 'user_history/ver_notas.html', {'notas':notas, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto, 'us':us})
    else:
        return HttpResponseRedirect('/index')
    
"""
def priorizar_us(us, proyecto):
    lista_sprints = proyecto.sprint.all().filter(estado=1)
    sprint = lista_sprints.order_by('id')[:1].get()
    
    us.reestimar = True
    us.id_sprint = 0
    us.save()
    
    ussp = US_Sprint(sprint=sprint, user_story=us)
    ussp.save()
"""   

""" Administración de Sprints. """
def index_sprint(request, user_id, proyecto_id):
    """
    Método de inicio que nos permite verificar todo lo relaciona a los sprint.
    
    @param request: Http request
    @type  request:HtpptRequest 
    @param user_id: Id de un usuario registrado en el sistema.
    @param proyecto_id: Id de un proyecto registrado en el sistema.
    @return: render al template user_history/index.html para la página de inicio.
             render al template user_history/results.html para obtener resultados de la búsqueda.  
             Listado de US.
    """  
    user = request.user
    accion = "Listar Sprint"
    
    staff = verificar_permiso(user, accion)
    
    if staff:
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
                
        saludo = saludo_dia()
        proyecto = Proyectos.objects.get(id=proyecto_id)
       
        us = proyecto.sprint.all().order_by('id')
        en_ejecucion = us.filter(estado=2)
        if en_ejecucion:
            en_ejecucion = us.get(estado=2)
        filax = us.count()
        filaz = us.exclude(estado=3).exclude(estado=4).count()          
        
        for sp in us:
            lUH = sp.listaUS.all()
            for uh in lUH:
                if not uh.usuario_asignado:
                    sp.activar = False
                    break
                else:
                    sp.activar = True
            sp.save()

        if request.method == 'POST':
            results = us
            form = BuscarSprintForm(request.POST)
                
            if form.is_valid():
                sid = request.POST.get('id', None)
                if sid:
                    results = results.filter(id__iexact=sid)
                snombre = request.POST.get('nombre', None)
                if snombre:
                    results = results.filter(nombre__icontains=snombre)
                
                
                if not sid and not snombre:
                    results = None
                    
                if results:
                    results.order_by('id')
                return render_to_response('sprints/results.html', {'user':user, 'proyecto':proyecto, 'saludo':saludo ,'us':us, 'results':results}, context_instance=RequestContext(request))
        else:
            form = BuscarSprintForm()
        return render_to_response('sprints/index.html', {'filaz':filaz, 'en_ejecucion':en_ejecucion, 'filax':filax, 'us':us, 'staff':staff, 'user':user, 'proyecto':proyecto, 'saludo':saludo}, context_instance=RequestContext(request)) 
    else:
        return HttpResponseRedirect('/index')


def crear_sprint(request, user_id, proyecto_id):
    
    """
    Método que nos permite crear un sprint nuevo relacionado a un proyecto.
    
    @param request: Http request
    @type  request:HtpptRequest 
    @param user_id: Id de un usuario registrado en el sistema.
    @param proyecto_id: Id de un proyecto registrado en el sistema.
    @return: render al template sprints/crear.html.  
    
    """
    
    usuario = request.user
    proyecto = Proyectos.objects.get(id=proyecto_id)
    accion = "Crear Sprint"
    
    staff = verificar_permiso(usuario, accion)
    
    if staff:
        aid = 1
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
        
        saludo = saludo_dia()
        if request.method == 'POST':
            form = CrearSprintForm(request.POST, proyecto_id=proyecto_id)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                nombre = cleaned_data.get('nombre')
                estado = cleaned_data.get('estado')
                
                sp = Sprint()
                sp.nombre = nombre
                sp.estado = estado
                
                sp.save()
                
                ps=Sprint_Proyectos(sprint=sp, proyecto=proyecto)
                ps.save()
                 
                return render_to_response('sprints/gracias.html', {'aid':aid, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto, 'sp':sp}, context_instance=RequestContext(request))
        else:
            form = CrearSprintForm(proyecto_id=proyecto_id)
        return render(request, 'sprints/crear.html', {'form': form, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto})
    else:
        return HttpResponseRedirect('/index')

def modificar_sprint(request, user_id, proyecto_id, sp_id):
    
    """
    Método que nos permite modificar un sprint relacionado a un proyecto.
    
    @param request: Http request
    @type  request:HtpptRequest 
    @param user_id: Id de un usuario registrado en el sistema.
    @param proyecto_id: Id de un proyecto registrado en el sistema.
    @return: render al template sprints/modificar.html.  
    
    """
    usuario = request.user
    proyecto = Proyectos.objects.get(id=proyecto_id)

    accion1 = "Modificar Sprint"
   

    staff1 = verificar_permiso(usuario, accion1)
    
    sp = proyecto.sprint.get(id=sp_id)
    if staff1:
        aid = 2
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
        
        saludo = saludo_dia()
        if request.method == 'POST':
            form = EditarSprintForm(request.POST, proyecto_id=proyecto_id, sp_id=sp_id)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                nombre = cleaned_data.get('nombre')
                duracion = cleaned_data.get('duracion')
                
                if nombre:
                    sp.nombre = nombre
                if duracion:
                    sp.duracion = duracion
                
                sp.save()
                
                return render_to_response('sprints/gracias.html', {'sp':sp, 'aid':aid, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto}, context_instance=RequestContext(request))
        else:
            form = EditarSprintForm(proyecto_id=proyecto_id, sp_id=sp_id)
        return render(request, 'sprints/modificar.html', {'form': form, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto, 'sp':sp, 'staff1':staff1})
    else:
        return HttpResponseRedirect('/index')
    
def ver_sprint(request, user_id, proyecto_id, sp_id):
    """
    Método que nos permite ver los sprints relacionado a un proyecto.
    
    @param request: Http request
    @type  request:HtpptRequest 
    @param user_id: Id de un usuario registrado en el sistema.
    @param proyecto_id: Id de un proyecto registrado en el sistema.
    @return: render al template sprints/ver.html.  
    
    """
    
    
    usuario = request.user
    proyecto = Proyectos.objects.get(id=proyecto_id)

    accion1 = "Visualizar Sprint"
   

    staff1 = verificar_permiso(usuario, accion1)
    
    sp = proyecto.sprint.get(id=sp_id)
    if staff1:
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
        
        saludo = saludo_dia()
        
        lista_us = sp.listaUS.all().order_by('prioridad_SM')
        lista_usuarios = sp.desarrolladores.all()
        
        return render(request, 'sprints/ver.html', {'lista_usuarios':lista_usuarios,'lista_us': lista_us, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto, 'sp':sp, 'staff1':staff1})
    else:
        return HttpResponseRedirect('/index')

def asignar_us_sprint(request, user_id, proyecto_id, sp_id):
    
    """
    Método que nos permite asignar user stories a sprints.
    
    @param request: Http request
    @type  request:HtpptRequest 
    @param user_id: Id de un usuario registrado en el sistema.
    @param proyecto_id: Id de un proyecto registrado en el sistema.
    @param sp_id: Id de un sprint registrado en el sistema.
    @return: render al template sprints/asignar.html.  
    
    """
    usuario = request.user
    proyecto = Proyectos.objects.get(id=proyecto_id)

    accion = "Asignar US a Sprint"
   

    staff = verificar_permiso(usuario, accion)
    
    usuarios = proyecto.usuarios.all().filter(asignado=False)
    
    sp = proyecto.sprint.get(id=sp_id)
    usuarios_sprint = sp.desarrolladores.all()
    
    us1 = proyecto.user_stories.all().filter(prioridad_SM=1).exclude(estado=2).exclude(estado=3).filter(id_sprint=None)
    us2 = proyecto.user_stories.all().filter(prioridad_SM=2).exclude(estado=2).exclude(estado=3).filter(id_sprint=None)
    us3 = proyecto.user_stories.all().filter(prioridad_SM=3).exclude(estado=2).exclude(estado=3).filter(id_sprint=None)
    user_stories = map(None, us1, us2, us3)
    
    if staff:
        aid = 3
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
        
        saludo = saludo_dia()
        sp_us = None
        if request.method == 'POST':

            lista_user_stories = request.POST.getlist(u'userstories')
            lista_usuarios = request.POST.getlist(u'lusuarios')
            lista_horas_por_dia = request.POST.getlist('lhoras_por_dia')
            while '' in lista_horas_por_dia:
                lista_horas_por_dia.remove('')
            if lista_user_stories and lista_usuarios:
                asignar_us_sp(request, sp_id, lista_user_stories, lista_usuarios, lista_horas_por_dia)
                sp_us1 = sp.listaUS.all().filter(prioridad_SM=1)
                sp_us2 = sp.listaUS.all().filter(prioridad_SM=2)
                sp_us3 = sp.listaUS.all().filter(prioridad_SM=3)
                sp_us = map(None, sp_us1, sp_us2, sp_us3)
                sp_desarrolladores = sp.desarrolladores.all()
            else:
                sp_us = None
                sp_desarrolladores = None
                
            return render_to_response('sprints/gracias.html', {'sp_desarrolladores':sp_desarrolladores, 'sp_us':sp_us, 'aid':aid, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto}, context_instance=RequestContext(request))

        return render(request, 'sprints/asignar.html', {'usuarios_sprint':usuarios_sprint, 'usuarios':usuarios, 'user_stories':user_stories, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto, 'sp':sp})
    else:
        return HttpResponseRedirect('/index')

def asignar_us_sp(request, sp_id, lista_user_stories, lista_usuarios, lista_horas_por_dia):
    
    """
    Método que realiza la acción de asignar user stories a sprints.
    
    @param request: Http request
    @type  request:HtpptRequest 
    @param sp_id: Id de un sprint registrado en el sistema.
    @return: Informa si el user story a sido asignado.  
    
    """
    sprint = get_object_or_404(Sprint, id=sp_id)
    ussp = None
    spus = None
    us_hp = None
    if lista_user_stories:
        for us_id in lista_user_stories:
            
            us = User_Story.objects.get(id=us_id)   
            spus = US_Sprint(sprint=sprint, user_story=us)
            spus.save()
            
            us.id_sprint = sp_id
            us.save()
        
        for us_id in lista_user_stories:
            us = User_Story.objects.get(id=us_id)
            tipo = us.tipo
            flujo = Flujos.objects.filter(tipo=tipo)
            if flujo:
                flujo = Flujos.objects.get(tipo=tipo)
            
                us_f = us_Flujos(flujo=flujo, us=us)
                us_f.save()
        
                us.id_flujo = flujo.id
                us.save()
            
    if lista_usuarios and lista_horas_por_dia:
        us_hp = map(None, lista_usuarios, lista_horas_por_dia)
        for user_id, h in us_hp:
            if user_id and h:
                user = Usuarios.objects.get(id=user_id)   
                ussp = Usuarios_Sprint(sprint=sprint, desarrolladores=user)
                ussp.save()
        
                horas = Horas(cantidad_diaria=h)
                horas.id_sprint = sp_id
                horas.id_usuario = user.id
                horas.save()
                
                user.horas_por_dia = horas
                user.save()
    return sprint

def cambiar_estado_sprint(request, user_id, proyecto_id, sp_id):
    """
    Método que nos permite cambiar el estado de un sprint especifico.
    
    @param request: Http request
    @type  request:HtpptRequest 
    @param user_id: Id de un usuario registrado en el sistema.
    @param proyecto_id: Id de un proyecto registrado en el sistema.
    @param sp_id: Id de un sprint registrado en el sistema.
    @return: render al template sprints/cambiar_estado.html.  
    
    """
    usuario = request.user
    proyecto = Proyectos.objects.get(id=proyecto_id)

    accion = "Cambiar estado Sprint"
   
    staff = verificar_permiso(usuario, accion)
    
    sp = proyecto.sprint.get(id=sp_id)
    
    if staff:
        aid = 4
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
        
        saludo = saludo_dia()
        lista_us = sp.listaUS.all()
        
        cambio_estado = True
        if sp.estado == 2:
            cambio_estado = False
        
        if request.method == 'POST':
            form = CambiarEstadoSprintForm(request.POST)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                estado = cleaned_data.get('estado')
                
                if estado:
                    sp.estado = estado
                
                if estado == 2:
                    sp.fechaInicio=datetime.now()
                    now=datetime.now()
                            
                    sp.fechaFin = date_by_adding_business_days(sp.fechaInicio, sp.duracion)
                
                if lista_us:
                    for us in lista_us:
                        if estado==2:
                            us.estado = 2
                            
                        elif estado==3:
                            us.estado = 3
                            
                        elif estado==4:
                            us.estado = 4
                            us.reestimar = True
                            
                            usuario_asignado = us.usuario_asignado
                            usuario_asignado = False
                            usuario_asignado.save()
                            
                        us.save()
                    
                sp.save()
                
                return render_to_response('sprints/gracias.html', {'sp':sp, 'aid':aid, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto}, context_instance=RequestContext(request))
        else:
            form = CambiarEstadoSprintForm()
        return render(request, 'sprints/cambiar_estado.html', {'cambio_estado':cambio_estado, 'lista_us':lista_us, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto, 'sp':sp})
    else:
        return HttpResponseRedirect('/index')


"Gestión de Flujos"
def crear_flujo(request, user_id, proyecto_id):
    """
    Método que nos permite crear un nuevo flujo para un proyecto dado.
    
    @param request: Http request
    @type  request:HtpptRequest 
    @param user_id: Id de un usuario registrado en el sistema.
    @param proyecto_id: Id de un proyecto registrado en el sistema.
    @return: render al template flujos/crear.html.  
    
    """
    usuario = request.user
    proyecto = Proyectos.objects.get(id=proyecto_id)
    accion = "Crear Flujo"
    
    staff = verificar_permiso(usuario, accion)
    
    if staff:
        aid = 1
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
        
        saludo = saludo_dia()
        tipos = Tipo.objects.all()
        tipo = None
        if request.method == 'POST':
            form = CrearFlujosForm(request.POST)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                nombre = cleaned_data.get('nombre')
                descripcion = cleaned_data.get('descripcion')
                tipo_id = cleaned_data.get('tipo_id')
                if tipo_id:
                    tipo = Tipo.objects.get(id=tipo_id)
                flujo = Flujos()
                flujo.nombre = nombre
                flujo.descripcion = descripcion
                flujo.tipo = tipo
                flujo.save()
                
                fp = Flujos_Proyectos(proyecto=proyecto, flujo=flujo)
                fp.save()
                
                
                return render_to_response('flujos/gracias.html', {'aid':aid, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto, 'flujo':flujo}, context_instance=RequestContext(request))
        else:
            form = CrearFlujosForm()
        return render(request, 'flujos/crear.html', {'form': form,'tipos':tipos, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto})
    else:
        return HttpResponseRedirect('/index')

def index_flujo(request, user_id, proyecto_id): 
    """
    Método de inicio para la gestion de flujos relacionado a proyectos existentes en el sistema.
    
    @param request: Http request
    @type  request:HtpptRequest 
    @param user_id: Id de un usuario registrado en el sistema.
    @param proyecto_id: Id de un proyecto registrado en el sistema.
    @return: render al template flujos/index.html.  
    
    """ 
    user = request.user
    accion = "Listar Flujo"
    
    staff = verificar_permiso(user, accion)
    
    if staff:
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
                
        saludo = saludo_dia()
        usuario = Usuarios.objects.get(id=user_id)
        proyecto = Proyectos.objects.get(id=proyecto_id)
        f_us = []
        flujo = proyecto.flujos.all()
        for f in flujo:
            us=f.us.all()    
            if not us:
                f_us.append(f)
                
        filax = flujo.count()
        if request.method == 'POST':
            results = proyecto.flujos.all().exclude(id=usuario.id)
            form = BuscarFlujosForm(request.POST)
                
            if form.is_valid():
                flujoid = request.POST.get('id', None)
                if flujoid:
                    results = results.filter(id__iexact=flujoid)
                
                flujonombre = request.POST.get('nombre', None)
                if flujonombre:
                    results = results.filter(nombre__iexact=flujonombre)
                            
                flujodescripcion = request.POST.get('descripcion', None)
                if flujodescripcion:
                    results = results.filter(descripcion__icontains=flujodescripcion)
                           
                
                if not flujoid and not flujodescripcion and not flujonombre:
                    results = None
                    
                if results:
                    results.order_by('id')
                return render_to_response('flujos/results.html', {'user':user,'f_us':f_us, 'proyecto':proyecto, 'saludo':saludo, 'results':results}, context_instance=RequestContext(request))
        else:
            form = BuscarFlujosForm()
        return render_to_response('flujos/index.html', {'filax':filax,'f_us':f_us, 'flujo':flujo, 'staff':staff, 'user':user, 'proyecto':proyecto, 'saludo':saludo}, context_instance=RequestContext(request)) 
    else:
        return HttpResponseRedirect('/index')

def crear_actividad(request, user_id, proyecto_id, flujo_id):
    """
    Método que nos permite crear una actividad nueva dentro de un flujo de un proyecto existente en el sistema.
    
    @param request: Http request
    @type  request:HtpptRequest 
    @param user_id: Id de un usuario registrado en el sistema.
    @param proyecto_id: Id de un proyecto registrado en el sistema.
    @param flujo_id: Id de un flujo registrado en el sistema.
    @return: render al template flujos/crear_actividades.html.  
    
    """
    usuario = request.user
    proyecto = Proyectos.objects.get(id=proyecto_id)
    flujo = proyecto.flujos.get(id=flujo_id)
    accion = "Crear Actividad"
    
    staff = verificar_permiso(usuario, accion)
    if staff:
        aid = 1
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
        
        saludo = saludo_dia()
        if request.method == 'POST':
            form = CrearActividadForm(request.POST)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                nombre = cleaned_data.get('nombre')
                descripcion = cleaned_data.get('descripcion')
                
                actividad = Actividades()
                actividad.nombre = nombre
                actividad.descripcion = descripcion
                actividad.save()
                
                af = Actividades_Flujos(actividad=actividad, flujo=flujo)
                af.save()
                
                
                
                return render_to_response('flujos/gracias_actividad.html', {'actividad':actividad, 'aid':aid, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto}, context_instance=RequestContext(request))
        else:
            form = CrearActividadForm()
        return render(request, 'flujos/crear_actividades.html', {'form': form, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto,'staff':staff})
    else:
        return HttpResponseRedirect('/index')

def visualizar_flujo(request, user_id, proyecto_id, flujo_id):
    """
    Método que nos permite visualizar flujos de un proyecto dado.
    
    @param request: Http request
    @type  request:HtpptRequest 
    @param user_id: Id de un usuario registrado en el sistema.
    @param proyecto_id: Id de un proyecto registrado en el sistema.
    @param flujo_id: Id de un flujo registrado en el sistema.
    @return: render al template flujos/visualizar_flujo.html.  
    
    """    
    usuario = request.user
    proyecto = Proyectos.objects.get(id=proyecto_id)
    flujo = proyecto.flujos.get(id=flujo_id)
    accion = "Visualizar Flujo"
    
    staff = verificar_permiso(usuario, accion)
    
    actividades=[]
    
    if staff:
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
            
        saludo = saludo_dia()
            
        flujo = get_object_or_404(Flujos, id=flujo_id)
        up = flujo.actividades.all()
        us = flujo.us.all()

        
        return render(request, 'flujos/visualizar_flujo.html', {'flujo':flujo,'us':us,  'up':up, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto})
    else:
        return HttpResponseRedirect('/index')

def modificar_flujo(request, user_id, proyecto_id, flujo_id):
    """
    Método que nos permite modificar flujos de un proyecto dado.
    
    @param request: Http request
    @type  request:HtpptRequest 
    @param user_id: Id de un usuario registrado en el sistema.
    @param proyecto_id: Id de un proyecto registrado en el sistema.
    @param flujo_id: Id de un flujo registrado en el sistema.
    @return: render al template flujos/modificar.html.  
    
    """
    usuario = request.user
    proyecto = Proyectos.objects.get(id=proyecto_id)

    accion1 = "Modificar Flujo"
   

    staff1 = verificar_permiso(usuario, accion1)
    flujo = proyecto.flujos.get(id=flujo_id)
    tipos = Tipo.objects.all()
    f_us = flujo.us.all()
    
    if staff1:
        aid = 2
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
        
        saludo = saludo_dia()
        if request.method == 'POST':
            form = EditarFlujoForm(request.POST)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                nombre = cleaned_data.get('nombre')
                descripcion = cleaned_data.get('descripcion')
                tipo_id = cleaned_data.get('tipo_id')
                if not f_us:
                    flujo.nombre = nombre
                    flujo.descripcion = descripcion
                    tipo = Tipo.objects.get(id=tipo_id)
                    flujo.tipo = tipo
                    
                    flujo.save()
                
                return render_to_response('flujos/gracias.html', {'flujo':flujo,'aid':aid, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto}, context_instance=RequestContext(request))
        else:
            form = EditarFlujoForm()
        return render(request, 'flujos/modificar.html', {'form':form,'tipos':tipos, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto, 'flujo':flujo, 'staff1':staff1})
    else:
        return HttpResponseRedirect('/index')

def modificar_actividad(request, user_id, proyecto_id, flujo_id, actividad_id):
    """
    Método que nos permite modificar la actividad de un flujo relacionado a un proyecto existente en el sistema.
    
    @param request: Http request
    @type  request:HtpptRequest 
    @param user_id: Id de un usuario registrado en el sistema.
    @param proyecto_id: Id de un proyecto registrado en el sistema.
    @param flujo_id: Id de un flujo registrado en el sistema.
    @param actividad_id: Id de una actividad registrada en el sistema.
    @return: render al flujos/modificar_actividad.html.  
    
    """
    usuario = request.user
    proyecto = Proyectos.objects.get(id=proyecto_id)

    accion1 = "Modificar Actividad"
   

    staff1 = verificar_permiso(usuario, accion1)
    flujo = proyecto.flujos.get(id=flujo_id)
    actividad = flujo.actividades.get(id=actividad_id)
    if staff1:
        aid = 2
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
        
        saludo = saludo_dia()
        if request.method == 'POST':
            form = EditarFlujoForm(request.POST)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                nombre = cleaned_data.get('nombre')
                descripcion = cleaned_data.get('descripcion')
                
                actividad.nombre = nombre
                actividad.descripcion = descripcion

                actividad.save()
                
                return render_to_response('flujos/gracias_actividad.html', {'actividad':actividad,'flujo':flujo,'aid':aid, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto}, context_instance=RequestContext(request))
        else:
            form = EditarActividadForm()
        return render(request, 'flujos/modificar_actividad.html', {'form':form, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto, 'actividad':actividad,'flujo':flujo, 'staff1':staff1})
    else:
        return HttpResponseRedirect('/index')

def cambiar_estado_flujo(request, user_id, proyecto_id, flujo_id):
    """
    Método que nos permite modificar el estado de un flujo.
    
    @param request: Http request
    @type  request:HtpptRequest 
    @param user_id: Id de un usuario registrado en el sistema.
    @param proyecto_id: Id de un proyecto registrado en el sistema.
    @param flujo_id: Id de un flujo registrado en el sistema.
    @return: render al flujos/cambiar_estado.html.  
    
    """
    usuario = request.user
    proyecto = Proyectos.objects.get(id=proyecto_id)

    accion = "Cambiar estado Flujo"
   
    staff = verificar_permiso(usuario, accion)
    
    f = proyecto.flujos.get(id=flujo_id)
    
    if staff:
        aid = 4
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
        
        saludo = saludo_dia()
        lista_us = f.us.all()
        if request.method == 'POST':
            form = CambiarEstadoFlujoForm(request.POST)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                estado = cleaned_data.get('estado')
 
                if not lista_us:
                        f.estado = estado
                        f.save()
                
                return render_to_response('flujos/gracias.html', {'flujo':f, 'aid':aid, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto}, context_instance=RequestContext(request))
        else:
            form = CambiarEstadoSprintForm()
        return render(request, 'flujos/cambiar_estado.html', {'lista_us':lista_us,'f':f, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto})
    else:
        return HttpResponseRedirect('/index')

def asignar_flujo(request, user_id, proyecto_id, flujo_id):
    """
    Método que nos permite asignar un flujo a un proyecto dado.
    
    @param request: Http request
    @type  request:HtpptRequest 
    @param user_id: Id de un usuario registrado en el sistema.
    @param proyecto_id: Id de un proyecto registrado en el sistema.
    @param flujo_id: Id de un flujo registrado en el sistema.
    @return: render al flujos/asignar.html.  
    
    """ 
    usuario = request.user
    proyecto = Proyectos.objects.get(id=proyecto_id)

    accion = "Asignar US a Flujo"
   

    staff = verificar_permiso(usuario, accion)
    
    f = proyecto.flujos.get(id=flujo_id)
    tipo = f.tipo
    us1 = proyecto.user_stories.all().filter(nivel_prioridad=1).filter(tipo=tipo)
    us2 = proyecto.user_stories.all().filter(nivel_prioridad=2).filter(tipo=tipo)
    us3 = proyecto.user_stories.all().filter(nivel_prioridad=3).filter(tipo=tipo)
    user_stories = map(None, us1, us2, us3)
    
    if staff:
        aid = 3
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
        
        saludo = saludo_dia()
        f_us = None
        if request.method == 'POST':

            lista_user_stories = request.POST.getlist(u'userstories')
            if lista_user_stories:     
                asignar_us_f(request, flujo_id, lista_user_stories)
                f_us1 = f.us.all().filter(nivel_prioridad=1).filter(tipo=tipo)
                f_us2 = f.us.all().filter(nivel_prioridad=2).filter(tipo=tipo)
                f_us3 = f.us.all().filter(nivel_prioridad=3).filter(tipo=tipo)
                f_us = map(None, f_us1, f_us2, f_us3)
                
            return render_to_response('flujos/gracias.html', {'f_us':f_us,'flujo':f, 'aid':aid, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto}, context_instance=RequestContext(request))

        return render(request, 'flujos/asignar.html', {'user_stories':user_stories, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto, 'f':f})
    else:
        return HttpResponseRedirect('/index')

def asignar_us_f(request, f_id, lista_user_stories):
    """
    Método que realiza la acción de asignar un user story a un flujo dado.
    
    @param request: Http request
    @type  request:HtpptRequest
    @param flujo_id: Id de un flujo registrado en el sistema.
    @return: Nos informa si el user story a sido asignado.  
    
    """ 
    flujo = get_object_or_404(Flujos, id=f_id)
    
    for us_id in lista_user_stories:
        
        us = User_Story.objects.get(id=us_id)   
        fus = us_Flujos(flujo=flujo, us=us)
        fus.save()
        
        us.id_flujo = f_id
        us.save()
       
    return fus

def visualizar_kanban(request, user_id, proyecto_id, flujo_id):


    usuario = request.user
    proyecto = Proyectos.objects.get(id=proyecto_id)
    flujo = proyecto.flujos.get(id=flujo_id)
    accion = "Kanban"
    
    staff = verificar_permiso(usuario, accion)
    
    
    if staff:
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
            
        saludo = saludo_dia()
            
        flujo = get_object_or_404(Flujos, id=flujo_id)
        up = flujo.actividades.all()
        us = flujo.us.all()

        
        return render(request, 'flujos/kanban.html', {'flujo':flujo,'us':us,  'up':up, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto})
    else:
        return HttpResponseRedirect('/index')
    
def cambiar_estado_kanban(request, user_id, proyecto_id, flujo_id, us_id):

    usuario = request.user
    proyecto = Proyectos.objects.get(id=proyecto_id)

    accion = "Kanban"
   
    staff = verificar_permiso(usuario, accion)
    
    flujo = proyecto.flujos.get(id=flujo_id)
    up = flujo.actividades.all()
    print up
    us = flujo.us.all()
    us1 = flujo.us.get(id=us_id)
    if staff:
        aid = 4
        comprobar(request)
        if(request.user.is_anonymous()):
            return HttpResponseRedirect('/ingresar')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['last_activity'] = str(now)
        
        saludo = saludo_dia()
        if request.method == 'POST':
            form = CambiarEstadoUSFlujoForm(request.POST)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                estado = cleaned_data.get('estado')
                
                ac_id = cleaned_data.get('actividad_id')
                if ac_id:
                    us1.f_actividad = ac_id
                    us1.f_estado = 1
                if estado:
                    us1.f_estado = estado
                us1.save()
                
                return render_to_response('flujos/kanban.html', {'us1':us1,'up':up, 'us':us,'flujo':flujo, 'aid':aid, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto}, context_instance=RequestContext(request))
        else:
            form = CambiarEstadoUSFlujoForm()
        return render(request, 'flujos/cambiar_estado_kanban.html', {'up':up,'us1':us1,'us':us,'flujo':flujo, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto})
    else:
        return HttpResponseRedirect('/index')



def saludo_dia():
    """
    Función de saludo. 
    @return: saludo: retorna un saludo (string) diferente dependiendo la hora del día.
    """
    hora = datetime.now().hour
    if hora >= 0 and hora < 6:
        saludo= "Buenas madrugadas"
    elif hora > 5 and hora < 12:
        saludo= "Buenos dias"
    elif hora >= 12 and hora <= 13:
        saludo= "Buena siesta"
    elif hora > 13 and hora <= 18:
        saludo= "Buenas tardes"
    elif hora >= 19 and hora <= 23:
        saludo= "Buenas noches"
        
    return saludo

def comprobar(request):
    """
    Verifica si el usuario a estado más de diez minutos inactivo,
    si es así se cierra la sesión.
    Verifica, además, que el usuario se encuentre autentificado, 
    si no es así, debe iniciar sesión.
    
    @param request:Http request    
    @type  request:HtpptRequest
    @return: redirige al template ingresar.html    
    
    """
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    now_object = datetime.strptime(now, '%Y-%m-%d %H:%M:%S')

    last_activity = request.session['last_activity']
    date_object = datetime.strptime(last_activity, '%Y-%m-%d %H:%M:%S')

    restaminutos = ((now_object - date_object).seconds)/60 
    
    if restaminutos >= 10:
        logout(request)
        return HttpResponseRedirect('/ingresar')

def verificar_permiso(usuario, accion):
    """
    Verifica si el usuario tiene un rol asociado, y si éste cuenta con el o los permisos necesarios,
    para realizar una acción determinada.
    
    @param usuario: objeto User registrado en el sistema.
    @param accion: string, que designa lo que quiere realizar el usuario.
    @return: staff: retorna True o False, dependiendo de si el usuario tiene o no permiso de realizar la acción. 
    
    """
    
    staff = None
    us = Usuarios.objects.get(id=usuario.id)
    
    if accion=="Registro de Usuarios" or accion=="Index de Usuarios" or accion=="Editar Usuarios" or accion=="Borrar Usuarios":
        permiso = Permisos.objects.filter(nombre="Administración de Usuarios")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.filter(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False
            
    if accion=="Ver Usuarios":
        permiso = Permisos.objects.filter(nombre="Consultar lista de Usuarios")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.filter(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False
    
    if accion=="Cambiar Estado":
        permiso = Permisos.objects.filter(nombre="Cambiar Estado del Usuario")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.filter(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False
    
    elif accion=="Asginar Rol a Usuarios en un Proyecto":
        permiso = Permisos.objects.filter(nombre="Asignación de Usuarios")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.filter(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False
    
    elif accion=="Ver Index de Admin":
        permiso = Permisos.objects.filter(nombre="Ver Página de Administración")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.filter(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False
    
    elif accion=="Ver Index de Usuario Regular":
        permiso = Permisos.objects.filter(nombre="Ver Página de Inicio")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.filter(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False
    
    elif accion=="Registro de Roles" or accion=="Index de Roles" or accion=="Editar Roles" or accion=="Borrar Roles" or accion=="Ver Roles":
        permiso = Permisos.objects.filter(nombre="Administración de Roles y Permisos")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.filter(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False
            
    elif accion=="Registro de Proyectos/Servicios" or accion=="Index de Proyectos/Servicios" or accion=="Editar Proyectos/Servicios" or accion=="Ver Proyectos/Servicios":
        permiso = Permisos.objects.filter(nombre="Administración de Proyectos/Servicios")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.filter(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False
        
    elif accion=="Definir Proyectos/Servicios":
        permiso = Permisos.objects.filter(nombre="Definición de Proyectos/Servicios")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.filter(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False
    
    elif accion=="Crear US":
        permiso = Permisos.objects.filter(nombre="Creación de US")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.filter(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False
            
    elif accion=="Desarrollar US":
        permiso = Permisos.objects.filter(nombre="Desarrollo de US")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.filter(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False
    
    elif accion=="Listar US":
        permiso = Permisos.objects.filter(nombre="Generar listado de US")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.filter(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False
    
    elif accion=="Modificar US - ValNeg":
        permiso = Permisos.objects.filter(nombre="Modificación de US - Valores de Negocios")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.filter(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False
    
    elif accion=="Modificar US - ValTec":
        permiso = Permisos.objects.filter(nombre="Modificación de US - Valor Técnico")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.filter(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False 
    
    elif accion=="Modificar US - Size":
        permiso = Permisos.objects.filter(nombre="Modificación de US - Size")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.filter(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False
            
    elif accion=="Modificar US - Prioridad":
        permiso = Permisos.objects.filter(nombre="Modificación de US - Prioridad")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.filter(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False 
    
    elif accion=="Modificar US - Notas":
        permiso = Permisos.objects.filter(nombre="Modificación de US - Notas")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.filter(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False 
    
    elif accion=="Modificar US - ArchAdj":
        permiso = Permisos.objects.filter(nombre="Modificación de US - Archivos adjuntos")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.filter(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False 
            
    elif accion=="Modificar US - Descripción":
        permiso = Permisos.objects.filter(nombre="Modificación de US - Descripción")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.filter(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False 
            
    elif accion=="Crear Tipo" or accion=="Modificar US - Tipo":
        permiso = Permisos.objects.filter(nombre="Modificación de US - Tipo")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.filter(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False
    
    elif accion=="Modificar US - TEst":
        permiso = Permisos.objects.filter(nombre="Modificación de US - Tiempo Estimado")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.filter(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False 
    
    elif accion=="Modificar US - TReal":
        permiso = Permisos.objects.filter(nombre="Modificación de US - Tiempo Real")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.filter(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False 
    
    elif accion=="Asignar US":
        permiso = Permisos.objects.filter(nombre="Asignación de US")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.filter(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False 
            
    elif accion=="Cambiar estado US" or accion=="Visualizar US":
        permiso = Permisos.objects.filter(nombre="Desarrollo de US")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.filter(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False
    
    elif accion=="Adjuntar archivo US":
        permiso = Permisos.objects.filter(nombre="Modificación de US - Archivos adjuntos")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.filter(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False
    
    elif accion=="Definir Prioridad SM":
        permiso = Permisos.objects.filter(nombre="Asignar Prioridad de Scrum Master al US")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.filter(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False
    
    elif accion=="Notas US":
        permiso = Permisos.objects.filter(nombre="Modificación de US - Notas")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.filter(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False
    
    elif accion=="Listar Sprint" or accion=="Crear Sprint" or accion=="Modificar Sprint" or accion=="Visualizar Sprint" or accion=="Asignar US a Sprint" or accion=="Cambiar estado Sprint":
        permiso = Permisos.objects.filter(nombre="Administración de Sprints")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.filter(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False
    
    elif accion=="Listar Flujo" or accion=="Crear Flujo" or accion == "Crear Actividad" or accion == "Visualizar Flujo" or accion == "Modificar Flujo" or accion == "Modificar Actividad" or accion == "Cambiar estado Flujo" or accion == "Asignar US a Flujo" or accion == "Kanban":
        permiso = Permisos.objects.filter(nombre="Administración de Flujos")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.filter(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False 
    return staff
    