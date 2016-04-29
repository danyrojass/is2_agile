# -*- encoding: utf-8 -*-
from django.shortcuts import get_object_or_404, render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.template import RequestContext
from datetime import datetime


from .forms import RegistroUserForm, EditarUserForm, BuscarUserForm

from .models import Usuarios


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
    staff= request.user.is_staff
    
    saludo= saludo_dia()
        
    if staff:
        return render_to_response('inicio_admin.html', {'usuario':usuario, 'saludo':saludo}, context_instance=RequestContext(request))    
    else:
        return render_to_response('inicio_usuario.html', {'usuario':usuario, 'saludo':saludo}, context_instance=RequestContext(request))   

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
    return render_to_response('creditos.html', {'usuario':usuario, 'saludo':saludo}, context_instance=RequestContext(request))    


def saludo_dia():
    """
    Funciones de saludo y comprobación de última actividad.
    
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



def index_usuarios(request):
    comprobar(request)
    if(request.user.is_anonymous()):
        return HttpResponseRedirect('/ingresar')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['last_activity'] = str(now)
    
    usuario = request.user
    saludo = saludo_dia()
    
    usuarios = User.objects.filter(is_active=True).order_by('id')
    filas= usuarios.count() - 1
    
    if request.method == 'POST':
        results = User.objects.filter(is_active=True)
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
                    results = results.filter(username__iexact=uusername)
                else:
                    results = None
                    
            uemail = request.POST.get('email', None)
            if uemail:
                if uemail != usuario.email:
                    results = results.filter(email__iexact=uemail)
                else:
                    results = None
                    
            first_name = request.POST.get('first_name', None)
            if first_name:
                if first_name != usuario.first_name:
                    results = results.filter(first_name__iexact=first_name)
                else:
                    results = None
                    
            last_name = request.POST.get('last_name', None)
            if last_name:
                if last_name != usuario.last_name:
                    results = results.filter(last_name__iexact=last_name)
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

@login_required(login_url='/ingresar')
def registrar_usuarios(request):
    """ 
    Registra a un Usuario al sistema.
    
    @param request:Http request
    @type  request:HtpptRequest
    @return: renderiza template registro.html
    
    
    """
    aid = 1
    comprobar(request)
    if(request.user.is_anonymous()):
        return HttpResponseRedirect('/ingresar')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['last_activity'] = str(now)
        
    usuario = request.user
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

@login_required(login_url='/ingresar')
def editar_usuarios(request, user_id):
    """ 
    Edita un Usuario del sistema.
    
    @param request:Http request
    @type  request:HtpptRequest
    @param user_id: Id de un usuario registrado  
    @return: renderiza template registro.html
    
    
    """
    aid = 2
    comprobar(request)
    if(request.user.is_anonymous()):
        return HttpResponseRedirect('/ingresar')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['last_activity'] = str(now)
    
    usuario = request.user
    saludo = saludo_dia()
    
    user_model = get_object_or_404(User, pk=user_id)
    user_profile = get_object_or_404(Usuarios, id=user_id)

    if request.method == 'POST':
        form = EditarUserForm(request.POST, request.FILES)
        if form.is_valid():
            user_model.email = form.cleaned_data['email']
            user_model.first_name = form.cleaned_data['first_name']
            user_model.last_name = form.cleaned_data['last_name']      
            user_model.save()
            
            user_profile.telefono = form.cleaned_data['telefono']
            user_profile.direccion = form.cleaned_data['direccion']
            user_profile.observacion = form.cleaned_data['observacion']
            user_profile.save()

            return render_to_response('usuarios/gracias.html', {'usuario':usuario, 'saludo':saludo, 'aid':aid, 'um':user_model, 'up':user_profile}, context_instance=RequestContext(request))
    else:
        form = EditarUserForm()
    return render(request, 'usuarios/editar.html', {'form': form, 'usuario':usuario, 'saludo':saludo, 'um':user_model, 'up':user_profile})

def eliminar_usuarios(request, user_id):
    """ 
    Redirige a eliminar un Usuario del sistema.
    
    @param request:Http request
    @type  request:HtpptRequest
    @param user_id: Id de un usuario registrado  
    @return: renderiza y redirige al template eliminar.html
    
    
    """
    comprobar(request)
    if(request.user.is_anonymous()):
        return HttpResponseRedirect('/ingresar')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['last_activity'] = str(now)
    
    usuario = request.user
    saludo = saludo_dia()
    
    user = get_object_or_404(User, pk=user_id)
    
    return render_to_response('usuarios/eliminar.html', {'usuario':usuario, 'saludo':saludo, 'user':user})

@login_required(login_url='/ingresar')
def delete_usuarios(request, user_id):
    """ 
    Elimina a un Usuario del sistema, es decir lo pone en estado inactivo.
    
    @param request:Http request
    @type  request:HtpptRequest
    @param user_id: Id de un usuario registrado  
    @return: renderiza template gracias.html
    
    
    """
    aid = 3
    usuario = request.user
    saludo = saludo_dia()
       
    user_model = get_object_or_404(User, pk=user_id)
    user_profile = get_object_or_404(Usuarios, id=user_id)
    
    user_model.is_active = False
    user_model.save()    
    return render_to_response('usuarios/gracias.html', {'usuario':usuario, 'saludo':saludo, 'um':user_model, 'up':user_profile, 'aid':aid}, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def ver_usuarios(request, user_id):
    """ 
    Muestra a un Usuario del sistema.
    
    @param request:Http request
    @type  request:HtpptRequest
    @param user_id: Id de un usuario registrado  
    @return: renderiza template ver.html
    
    
    """
    comprobar(request)
    if(request.user.is_anonymous()):
        return HttpResponseRedirect('/ingresar')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['last_activity'] = str(now)
    
    usuario = request.user
    saludo = saludo_dia()
    
    user_model = get_object_or_404(User, pk=user_id)
    user_profile = get_object_or_404(Usuarios, id=user_id)
    
    return render_to_response('usuarios/ver.html', {'usuario':usuario, 'saludo':saludo, 'um':user_model, 'up':user_profile})
