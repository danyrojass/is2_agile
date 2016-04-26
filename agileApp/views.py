# -*- encoding: utf-8 -*-
from django.shortcuts import get_object_or_404, render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.template import RequestContext
from datetime import datetime
from .forms import RegistroUserForm, EditarUserForm, BuscarUserForm, CrearRolForm, BuscarRolForm,\
EditarRolForm, ModificarContrasenaForm, CrearProyectoForm, DefinirProyectoForm, BuscarProyectoForm,\
EditarProyectoForm, ElegirProyectoForm, AsignarRolForm
from .models import Usuarios, Permisos, Roles, Permisos_Roles, Usuarios, Proyectos, Roles_Usuarios_Proyectos,\
Usuarios_Proyectos, Roles_Usuarios
from django.contrib.auth.hashers import make_password

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
        if request.method == 'POST':
            form = ElegirProyectoForm(request.POST, request.FILES)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                proyecto_id = cleaned_data.get('proyecto_id')
                proyecto = Proyectos.objects.filter(id=proyecto_id)
                return render_to_response('inicio_usuario.html', {'usuario':usuario, 'proyecto':proyecto, 'saludo':saludo}, context_instance=RequestContext(request))   

        else:
            form = ElegirProyectoForm()
            
        return render(request, 'elegir_proyecto.html', {'usuario':usuario, 'proyectos':proyectos, 'saludo':saludo, 'form': form})
    
def creditos(request):
    """
    Método que se encarga de mostrar los créditos del sistema.
    
    @param request:Http request
    @type  request:HtpptRequest
    @return: render al template de creditos.html
    
    """
    comprobar(request)        
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

        saludo = saludo_dia()
        
        usuarios = User.objects.order_by('id')
        filas= usuarios.count() - 1
        
        if request.method == 'POST':
            results = User.objects.all().exclude(id=1)
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
                        results = results.filter(username__contains=uusername)
                    else:
                        results = None
                        
                uemail = request.POST.get('email', None)
                if uemail:
                    if uemail != usuario.email:
                        results = results.filter(email__contains=uemail)
                    else:
                        results = None
                        
                first_name = request.POST.get('first_name', None)
                if first_name:
                    if first_name != usuario.first_name:
                        results = results.filter(first_name__contains=first_name)
                    else:
                        results = None
                        
                last_name = request.POST.get('last_name', None)
                if last_name:
                    if last_name != usuario.last_name:
                        results = results.filter(last_name__contains=last_name)
                    else:
                        results = None
                        
                if not uid and not uusername and not uemail and not first_name and not last_name:
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
    @return: renderiza template de .html
    
    
    """
    usuario = request.user
    accion = "Registro de Usuarios"
    
    staff = verificar_permiso(usuario, accion)
    
    if staff:
        aid = 1
        comprobar(request)
        
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
    usuario = request.user
    accion = "Editar Usuarios"
    
    staff = verificar_permiso(usuario, accion)
    
    if staff:
        
        aid = 2
        comprobar(request)
        
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
    else:
        return HttpResponseRedirect('/index')

def eliminar_usuarios(request, user_id):
    usuario = request.user
    accion = "Borrar Usuarios"
    
    staff = verificar_permiso(usuario, accion)
    
    if staff:
        comprobar(request)

        saludo = saludo_dia()
        
        user = get_object_or_404(User, pk=user_id)
        
        return render_to_response('usuarios/eliminar.html', {'usuario':usuario, 'saludo':saludo, 'user':user})
    else:
        return HttpResponseRedirect('/index')

@login_required(login_url='/ingresar')
def delete_usuarios(request, user_id):
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
    usuario = request.user
    accion = "Ver Usuarios"
    
    staff = verificar_permiso(usuario, accion)
    
    if staff:
        comprobar(request)

        saludo = saludo_dia()
        
        user_model = get_object_or_404(User, pk=user_id)
        user_profile = get_object_or_404(Usuarios, id=user_id)
        
        return render_to_response('usuarios/ver.html', {'usuario':usuario, 'saludo':saludo, 'um':user_model, 'up':user_profile})
    else:
        return HttpResponseRedirect('/index')

def asignar_roles_usuarios_proyecto(request, user_id):
    """
    Método que permite asignar un Rol a un Usuario en un Proyecto determinado.
    
    @param request: Http request
    @param user_id: Id de un usuario registrado en el sistema.
    @return: render al template usuarios/asignar.html para la asignación. 
             render al template usuarios/gracias.html cuando se ha asignado correctamente.
    """
    
    usuario = request.user
    accion = "Asginar Rol a Usuarios en un Proyecto"
    
    staff = verificar_permiso(usuario, accion)
    
    if staff:
        aid = 5
        comprobar(request)
        
        saludo = saludo_dia()
        
        user_profile = get_object_or_404(Usuarios, id=user_id)
        user_model = get_object_or_404(User, id=user_id)
        roles = Roles.objects.filter(estado=True).exclude(nombre="Administrador")
        proyectos = Proyectos.objects.all().exclude(usuarios__id=user_id)
        if user_model.is_active:
            if request.method == 'POST':
                form = AsignarRolForm(request.POST)
                if form.is_valid():
                    rol_id = request.POST.get('rol_id', None)
                    proyecto_id = request.POST.get('proyecto_id', None)
                    
                    rol = get_object_or_404(Roles, id=rol_id) 
                    proyecto = get_object_or_404(Proyectos, id=proyecto_id)
                    
                    ru = Roles_Usuarios(roles=rol, usuario=user_profile)
                    ru.save()
                    
                    up = Usuarios_Proyectos(proyecto=proyecto, usuarios=user_profile)
                    up.save()
                    
                    rup = Roles_Usuarios_Proyectos(roles=rol, proyecto=proyecto, usuarios=user_profile)
                    rup.save()
                    
                    return render_to_response('usuarios/gracias.html', {'aid':aid, 'usuario':usuario, 'saludo':saludo, 'um':user_model, 'p':proyecto, 'r':rol}, context_instance=RequestContext(request))
            else:
                form = AsignarRolForm()
            return render(request, 'usuarios/asignar.html', {'form': form, 'roles':roles, 'proyectos':proyectos, 'usuario':usuario, 'saludo':saludo, 'um':user_model, 'up':user_profile})
    else:
        return HttpResponseRedirect('/index')

"""Administración de Roles"""
def crear_roles(request):
    usuario = request.user
    accion = "Registro de Roles"
    
    staff = verificar_permiso(usuario, accion)
    
    if staff:
        aid = 1
        comprobar(request)

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
    rol = get_object_or_404(Roles, id=rol_id)
    
    for p in lista_permisos:
        
        permiso = Permisos.objects.get(pk=p)   
        pr = Permisos_Roles(permisos=permiso, roles=rol)
        pr.save()
       
    return pr

def editar_roles(request, rol_id):
    usuario = request.user
    accion = "Editar Roles"
    
    staff = verificar_permiso(usuario, accion)
    
    if staff:
        aid = 2
        comprobar(request)
            
        saludo = saludo_dia()
            
        permisos1 = Permisos.objects.all().filter(nivel=1)
        permisos2 = Permisos.objects.all().filter(nivel=2)
        permisos3 = Permisos.objects.all().filter(nivel=3)
        permisos = map(None, permisos1, permisos2, permisos3)
            
        rol = get_object_or_404(Roles, id=rol_id)
        p1 = rol.permisos.all().filter(nivel=1)
        p2 = rol.permisos.all().filter(nivel=2)
        p3 = rol.permisos.all().filter(nivel=3)
        lista = map(None, p1, p2, p3)
        
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
        return render(request, 'roles/editar.html', {'form': form, 'usuario':usuario, 'saludo':saludo, 'rol':rol, 'lista':lista, 'permisos':permisos})
    else:
        return HttpResponseRedirect('/index')
    
def editar_permisos_rol(request, rol_id, lista_permisos):
    
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
    usuario = request.user
    accion = "Ver Roles"
    
    staff = verificar_permiso(usuario, accion)
    
    if staff:
        comprobar(request)
            
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
    usuario = request.user
    accion = "Borrar Roles"
    
    staff = verificar_permiso(usuario, accion)
    
    if staff:
        comprobar(request)
            
        usuario = request.user
        saludo = saludo_dia()
            
        rol = get_object_or_404(Roles, id=rol_id)
            
        return render_to_response('roles/eliminar.html', {'usuario':usuario, 'saludo':saludo, 'rol':rol})
    else:
        return HttpResponseRedirect('/index')
    
def delete_roles(request, rol_id):
    usuario = request.user
    accion = "Borrar Roles"
    
    staff = verificar_permiso(usuario, accion)
    
    if staff:
        aid = 3
        comprobar(request)
            
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
    usuario = request.user
    accion = "Index de Roles"
    
    staff = verificar_permiso(usuario, accion)
    
    if staff:
        comprobar(request)
            
        saludo = saludo_dia()
            
        roles = Roles.objects.order_by('id')
        roles = roles.exclude(nombre="Administrador")
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
                    results = results.filter(nombre__contains=rnombre)
                    
                robservacion = request.POST.get('observacion', None)
                if robservacion:
                    results = results.filter(observacion__contains=robservacion)
                            
                    if not rid and not rnombre and not robservacion:
                        results = None
                    
                    if results:
                        results.order_by('id')
                    return render_to_response('roles/results.html', {'usuario':usuario, 'saludo':saludo, 'results':results}, context_instance=RequestContext(request))
        else:
            form = BuscarRolForm()
            
        return render(request, 'roles/index.html', {'usuario':usuario, 'saludo':saludo, 'roles':roles, 'filas':filas})
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
            
        saludo = saludo_dia()
            
        if request.method == 'POST':
            form = CrearProyectoForm(request.POST, request.FILES)
            
            if form.is_valid():
                cleaned_data = form.cleaned_data
                nombre_largo = cleaned_data.get('nombre_largo')
            
                proyecto = Proyectos()
                proyecto.nombre_largo = nombre_largo
                proyecto.estado = 1
                proyecto.save()
                    
                return render_to_response('proyectos/gracias.html', {'aid':aid, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto}, context_instance=RequestContext(request))
        
        else:
            form = CrearProyectoForm()
            
        return render(request, 'proyectos/crear.html', {'usuario':usuario, 'saludo':saludo, 'form': form})
    else:
        return HttpResponseRedirect('/index')
    
def definir_proyectos(request, proyecto_id):
    """
    Metodo que define los parametros de un proyecto
    
    @param request: Http request
    @param request: proyecto_id
    @return: render al template proyectos/gracias.html
    """
    usuario = request.user
    accion = "Definir Proyectos/Servicios"
    
    staff = verificar_permiso(usuario, accion)
    
    if staff:
        aid = 2
        comprobar(request)
             
        saludo = saludo_dia()
            
        proyecto = get_object_or_404(Proyectos, id=proyecto_id)
            
        if request.method == 'POST':
            form = DefinirProyectoForm(request.POST, request.FILES)
            
            if form.is_valid():
                cleaned_data = form.cleaned_data
                nombre_corto = cleaned_data.get('nombre_corto')
                tipo = cleaned_data.get('tipo')
                descripcion = cleaned_data.get('descripcion')
                fecha_inicio = cleaned_data.get('fecha_inicio')
                fecha_fin_estimado = cleaned_data.get('fecha_fin_estimado')
                observaciones = cleaned_data.get('observaciones')
            
                proyecto.nombre_corto = nombre_corto
                proyecto.tipo = tipo
                proyecto.descripcion = descripcion
                proyecto.fecha_inicio = fecha_inicio
                proyecto.fecha_fin_estimado = fecha_fin_estimado
                proyecto.observaciones = observaciones
                proyecto.estado = 1
                proyecto.save()
                    
                return render_to_response('proyectos/gracias.html', {'aid':aid, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto}, context_instance=RequestContext(request))
        
        else:
            form = DefinirProyectoForm()
            
        return render(request, 'proyectos/definir.html', {'usuario':usuario, 'saludo':saludo, 'form': form})
    else:
        return HttpResponseRedirect('/index')
    
def editar_proyectos(request, proyecto_id):
    """
    Metodo que edita los parametros de un proyecto
    
    @param request: Http request
    @param request: proyecto_id
    @return: render al template proyectos/gracias.html
    """
    usuario = request.user
    accion = "Editar Proyectos/Servicios"
    
    staff = verificar_permiso(usuario, accion)
    
    if staff:
        aid = 3
        comprobar(request)
            
        saludo = saludo_dia()
            
        proyecto = get_object_or_404(Proyectos, id=proyecto_id)
            
        if request.method == 'POST':
            form = EditarProyectoForm(request.POST, request.FILES)
            
            if form.is_valid():
                cleaned_data = form.cleaned_data
                nombre_corto = cleaned_data.get('nombre_corto')
                tipo = cleaned_data.get('tipo')
                descripcion = cleaned_data.get('descripcion')
                fecha_inicio = cleaned_data.get('fecha_inicio')
                fecha_fin_estimado = cleaned_data.get('fecha_fin_estimado')
                observaciones = cleaned_data.get('observaciones')
            
                proyecto.nombre_corto = nombre_corto
                proyecto.tipo = tipo
                proyecto.descripcion = descripcion
                proyecto.fecha_inicio = fecha_inicio
                proyecto.fecha_fin_estimado = fecha_fin_estimado
                proyecto.observaciones = observaciones
                proyecto.save()
                    
                return render_to_response('proyectos/gracias.html', {'aid':aid, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto}, context_instance=RequestContext(request))
        
        else:
            form = EditarProyectoForm()
            
        return render(request, 'proyectos/editar.html', {'usuario':usuario, 'saludo':saludo, 'form': form, 'proyecto':proyecto})
    else:
        return HttpResponseRedirect('/index')
    
def ver_proyectos(request, proyecto_id):
    """
    Metodo que permite visualizar el proyecto seleccionado
    
    @param request: Http request
    @param request: proyecto_id
    @return: render al template proyectos/ver.html
    """
    usuario = request.user
    accion = "Ver Proyectos/Servicios"
    
    staff = verificar_permiso(usuario, accion)
    
    roles=[]
    
    if staff:
        comprobar(request)
            
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
    @return: render al template proyectos/results.html
    """
    usuario = request.user
    accion = "Index de Proyectos/Servicios"
    
    staff = verificar_permiso(usuario, accion)
    
    if staff:
        comprobar(request)
            
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
                    results = results.filter(nombre_largo__contains=pnombre_largo)
                    
                pnombre_corto = request.POST.get('nombre_corto', None)
                if pnombre_corto:
                    results = results.filter(nombre_corto__contains=pnombre_corto)
                    
                pdescripcion = request.POST.get('descripcion', None)
                if pdescripcion:
                    results = results.filter(descripcion_contains=pdescripcion)
                            
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
    
    if(request.user.is_anonymous()):
        return HttpResponseRedirect('/ingresar')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['last_activity'] = str(now)

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
    
    if accion=="Registro de Usuarios" or accion=="Index de Usuarios" or accion=="Editar Usuarios" or accion=="Borrar Usuarios" or accion=="Ver Usuarios":
        permiso = Permisos.objects.filter(nombre="Administración de Usuarios")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.get(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False
        
    elif accion=="Asginar Rol a Usuarios en un Proyecto":
        permiso = Permisos.objects.filter(nombre="Asignación de Usuarios")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.get(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False
    
    elif accion=="Ver Index de Admin":
        permiso = Permisos.objects.filter(nombre="Ver Página de Administración")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.get(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False
    
    elif accion=="Ver Index de Usuario Regular":
        permiso = Permisos.objects.filter(nombre="Ver Página de Inicio")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.get(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False
    
    elif accion=="Registro de Roles" or accion=="Index de Roles" or accion=="Editar Roles" or accion=="Borrar Roles" or accion=="Ver Roles":
        permiso = Permisos.objects.filter(nombre="Administración de Roles y Permisos")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.get(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False
            
    elif accion=="Registro de Proyectos/Servicios" or accion=="Index de Proyectos/Servicios" or accion=="Editar Proyectos/Servicios" or accion=="Ver Proyectos/Servicios":
        permiso = Permisos.objects.filter(nombre="Administración de Proyectos/Servicios")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.get(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False
        
    elif accion=="Definir Proyectos/Servicios":
        permiso = Permisos.objects.filter(nombre="Definición de Proyectos/Servicios")
        rol = Roles.objects.filter(permisos=permiso)
        rol_usuario_profile = Usuarios.objects.get(roles=rol, id=us.id)
        
        if rol_usuario_profile:
            staff = True
        else:
            staff = False
            
    return staff
    