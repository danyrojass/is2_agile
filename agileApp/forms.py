# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
import string
from .models import Roles, Proyectos, Usuarios_Proyectos, User_Story, Flujos
from django.shortcuts import get_object_or_404
from agileApp.models import Nota

 
TIPOS = ( 
    ( 'cl', 'Cliente' ),
    ( 'ur', 'Usuario Regular'),
)
    
class RegistroUserForm(forms.Form):
    id = 0
    username = forms.CharField(min_length=5)
    email = forms.EmailField()
    password = forms.CharField(min_length=10)
    password2 = forms.CharField(min_length=10)
    telefono = forms.CharField(required=False, max_length=15)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    direccion = forms.CharField(required=False, max_length=45)
    tipo = forms.ChoiceField(choices=TIPOS)
    observacion = forms.CharField(required=False, max_length=50)

    def clean_username(self):
        """Comprueba que no exista un username igual en la db"""
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise forms.ValidationError('Nombre de usuario ya registrado.')
        return username
    
    def clean_password2(self):
        """Comprueba que password y password2 sean iguales."""
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        # Setup Our Lists of Characters and Numbers
        characters = list(string.letters)
        numbers = [str(i) for i in range(10)]
        special_characters = list(string.punctuation)
        
        # Assume False until Proven Otherwise
        numCheck = False
        charCheck = False
        spcecialcharCheck = False

        # Loop until we Match        
        for char in password: 
            if not charCheck:
                if char in characters:
                    charCheck = True
            if not numCheck:
                if char in numbers:
                    numCheck = True
            if not spcecialcharCheck:
                if char in special_characters:
                    spcecialcharCheck = True
            if (numCheck and charCheck) and spcecialcharCheck:
                break
        
        if (not numCheck or not charCheck) or not spcecialcharCheck:
            raise forms.ValidationError('Su contraseña debe incluir al menos un número y un caracter no alfanumérico.')

        if password != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2
    
class EditarUserForm(forms.Form):
    def clean_password2(self):
        """Comprueba que password y password2 sean iguales."""
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        # Setup Our Lists of Characters and Numbers
        characters = list(string.letters)
        numbers = [str(i) for i in range(10)]
        special_characters = list(string.punctuation)
        
        # Assume False until Proven Otherwise
        numCheck = False
        charCheck = False
        spcecialcharCheck = False

        # Loop until we Match        
        for char in password: 
            if not charCheck:
                if char in characters:
                    charCheck = True
            if not numCheck:
                if char in numbers:
                    numCheck = True
            if not spcecialcharCheck:
                if char in special_characters:
                    spcecialcharCheck = True
            if (numCheck and charCheck) and spcecialcharCheck:
                break
        
        if password and password2:
            if (not numCheck or not charCheck) or not spcecialcharCheck:
                raise forms.ValidationError('Su contraseña debe incluir al menos un número y un caracter no alfanumérico.')
    
            if password != password2:
                raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2
    
    email = forms.EmailField()
    password = forms.CharField(min_length=10, required=False)
    password2 = forms.CharField(min_length=10, required=False)
    telefono = forms.CharField(required=False, max_length=15)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    direccion = forms.CharField(required=False, max_length=45)
    observacion = forms.CharField(required=False, max_length=50)
    estado = forms.BooleanField(required=False)
    
class ModificarContrasenaForm(forms.Form):
    actual_password = forms.CharField(min_length=10)
    password = forms.CharField(min_length=10)
    password2 = forms.CharField(min_length=10)
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        return super(ModificarContrasenaForm, self).__init__(*args, **kwargs)
    
    def clean_password_actual(self):
        """Comprueba que no exista un nombre igual en la db"""
        actual_password = self.cleaned_data['actual_password']
        if not self.user.check_password(actual_password):
            raise forms.ValidationError('La contraseña no coincide con la actual.')
        return actual_password
    
    def clean_password2(self):
        """Comprueba que password y password2 sean iguales."""
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        # Setup Our Lists of Characters and Numbers
        characters = list(string.letters)
        numbers = [str(i) for i in range(10)]
        special_characters = list(string.punctuation)
        
        # Assume False until Proven Otherwise
        numCheck = False
        charCheck = False
        spcecialcharCheck = False

        # Loop until we Match        
        for char in password: 
            if not charCheck:
                if char in characters:
                    charCheck = True
            if not numCheck:
                if char in numbers:
                    numCheck = True
            if not spcecialcharCheck:
                if char in special_characters:
                    spcecialcharCheck = True
            if (numCheck and charCheck) and spcecialcharCheck:
                break
        
        if (not numCheck or not charCheck) or not spcecialcharCheck:
            raise forms.ValidationError('Su contraseña debe incluir al menos un número y un caracter no alfanumérico.')

        if password != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2

class BuscarUserForm(forms.Form):
    id = forms.IntegerField(required=False)
    username = forms.CharField(required=False)
    email = forms.CharField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    tipo = forms.ChoiceField(choices=TIPOS, required=False)
        
class CrearRolForm(forms.Form):
    nombre = forms.CharField(max_length=25)
    tipo = forms.BooleanField(required=False)
    estado = forms.BooleanField(required=False)
    observacion = forms.CharField(max_length=50, required=False)
    
    def clean_nombre(self):
        """Comprueba que no exista un nombre igual en la db"""
        nombre = self.cleaned_data['nombre']
        if Roles.objects.filter(nombre=nombre):
            raise forms.ValidationError('Nombre de rol ya registrado.')
        return nombre
    
class BuscarRolForm(forms.Form):
    id = forms.IntegerField(required=False)
    nombre = forms.CharField(required=False)
    observacion = forms.CharField(required=False)
    
class EditarRolForm(forms.Form):
    nombre = forms.CharField(max_length=25)
    tipo = forms.BooleanField(required=False)
    observacion = forms.CharField(max_length=50, required=False)
    
    def __init__(self, *args, **kwargs):
        self.rol_id = kwargs.pop('rol_id')
        return super(EditarRolForm, self).__init__(*args, **kwargs)
        
    def clean_nombre(self):
        """Comprueba que no exista un nombre igual en la db"""
        nombre = self.cleaned_data['nombre']
        
        if Roles.objects.filter(nombre=nombre).exclude(id=self.rol_id):
            raise forms.ValidationError('Nombre de rol ya registrado.')
        return nombre

class AsignarRolForm(forms.Form):
    rol_id = forms.IntegerField()
    userd_id = forms.IntegerField()
    
class CrearProyectoForm(forms.Form):
    nombre_largo = forms.CharField(max_length=25)
    user_id = forms.IntegerField()
    
    def clean_nombre_largo(self):
        """Comprueba que no exista un nombre igual en la db"""
        nombre_largo = self.cleaned_data['nombre_largo']
        
        if Proyectos.objects.filter(nombre_largo=nombre_largo):
            raise forms.ValidationError('Nombre de proyecto ya registrado.')
        return nombre_largo
    
class DefinirProyectoForm(forms.Form):
    nombre_corto = forms.CharField(max_length=10)
    tipo = forms.BooleanField()
    estado = forms.IntegerField()
    descripcion = forms.CharField(max_length=50, required=False)
    fecha_inicio = forms.DateField()
    fecha_fin_estimado = forms.DateField()

class BuscarProyectoForm(forms.Form):
    id = forms.IntegerField(required=False)
    nombre_largo = forms.CharField(required=False)
    nombre_corto = forms.CharField(required=False)
    descripcion = forms.CharField(required=False)
    
class EditarProyectoForm(forms.Form):
    observaciones = forms.CharField(max_length=50, required=False)
    user_id = forms.IntegerField(required=False)
    
class CambiarEstadoForm(forms.Form):
    estado = forms.BooleanField(required=False)
    
class CrearUSForm(forms.Form):
    nombre = forms.CharField(max_length = 50)
    descripcion = forms.CharField(max_length = 50, required=False)
    prioridad_SM  = forms.CharField(max_length = 50, required=False)
    nivel_prioridad = forms.IntegerField(required=False)
    valor_negocios = forms.IntegerField(required=False)
    urgencia = forms.IntegerField(required=False)
    size = forms.IntegerField(required=False)
    tiempo_estimado = forms.IntegerField(required=False)
    tipo = forms.CharField(max_length = 50, required=False)
    tipo_creado = forms.CharField(max_length = 50, required=False)
    
    def __init__(self, *args, **kwargs):
        self.proyecto_id = kwargs.pop('proyecto_id')
        return super(CrearUSForm, self).__init__(*args, **kwargs)
        
    def clean_nombre(self):
        """Comprueba que no exista un nombre igual en el proyecto."""
        nombre = self.cleaned_data['nombre']
        proyecto = Proyectos.objects.get(id=self.proyecto_id)
        
        if proyecto.user_stories.filter(nombre=nombre):
            raise forms.ValidationError('Nombre de user story ya registrado.')
        return nombre

class BuscarUSForm(forms.Form):
    id = forms.IntegerField(required=False)
    nombre = forms.CharField(max_length = 50, required=False)
    descripcion = forms.CharField(max_length = 50, required=False)

class EditarUSForm(forms.Form):
    descripcion = forms.CharField(max_length = 50, required=False)
    nivel_prioridad = forms.IntegerField(required=False)
    valor_negocios = forms.IntegerField(required=False)
    urgencia = forms.IntegerField(required=False)
    size = forms.IntegerField(required=False)
    tiempo_estimado = forms.IntegerField(required=False)
    tipo = forms.CharField(max_length = 50, required=False)
    estado = forms.IntegerField(required=False)

class AsignarUSForm(forms.Form):
    id_user = forms.IntegerField()

class CambiarEstadoUSForm(forms.Form):
    estado = forms.IntegerField(required=False)
    tiempo_real = forms.IntegerField(required=False)   

class ReportarUSForm(forms.Form):
    descripcion = forms.CharField(max_length=50, required=False)
    horas_consumidas = forms.IntegerField(required=False)

class archivoUSForm(forms.Form):
    nombre = forms.CharField(max_length=25)
    archivo= forms.FileField()


class CrearSprintForm(forms.Form):
    nombre = forms.CharField(max_length=25)
    estado = forms.IntegerField()
    duracion = forms.IntegerField()
    
    def __init__(self, *args, **kwargs):
        self.proyecto_id = kwargs.pop('proyecto_id')
        return super(CrearSprintForm, self).__init__(*args, **kwargs)
        
    def clean_nombre(self):
        """Comprueba que no exista un nombre igual en el proyecto."""
        nombre = self.cleaned_data['nombre']
        proyecto = Proyectos.objects.get(id=self.proyecto_id)
        
        if proyecto.sprint.filter(nombre=nombre):
            raise forms.ValidationError('Nombre de sprint ya registrado.')
        return nombre

class BuscarSprintForm(forms.Form):
    id=forms.IntegerField(required=False)
    nombre = forms.CharField(max_length=25, required=False)

class EditarSprintForm(forms.Form):    
    nombre = forms.CharField(max_length=25, required=False)
    duracion = forms.IntegerField(required=False)
    
    def __init__(self, *args, **kwargs):
        self.proyecto_id = kwargs.pop('proyecto_id')
        self.sp_id = kwargs.pop('sp_id')
        return super(EditarSprintForm, self).__init__(*args, **kwargs)
        
    def clean_nombre(self):
        """Comprueba que no exista un nombre igual en el proyecto."""
        nombre = self.cleaned_data['nombre']
        proyecto = Proyectos.objects.get(id=self.proyecto_id)
        
        if proyecto.sprint.filter(nombre=nombre).exclude(id=self.sp_id):
            raise forms.ValidationError('Nombre de sprint ya registrado.')
        return nombre

class CambiarEstadoSprintForm(forms.Form):
    estado = forms.IntegerField(required=False)
    

class CrearFlujosForm(forms.Form):
    nombre = forms.CharField(max_length = 30)
    descripcion = forms.CharField(max_length=50)
    tipo_id = forms.IntegerField(required=False) 
    estado = forms.BooleanField(required=False)


class BuscarFlujosForm(forms.Form):
    id = forms.IntegerField(required=False)
    nombre = forms.CharField(max_length = 30)
    descripcion = forms.CharField(max_length=50, required=False)

class CrearActividadForm(forms.Form):
    nombre = forms.CharField(max_length=20)
    descripcion = forms.CharField(max_length=30, required=False)
    estado = forms.IntegerField(required=False)
    
    
class BuscarFlujoForm(forms.Form):
    id=forms.IntegerField(required=False)
    nombre = forms.CharField(max_length=25, required=False)

class EditarFlujoForm(forms.Form):    
    nombre = forms.CharField(max_length=30)
    descripcion = forms.CharField(max_length=50, required=False)
    tipo_id = forms.IntegerField(required=False)
    
class EditarActividadForm(forms.Form):    
    nombre = forms.CharField(max_length=20)
    descripcion = forms.CharField(max_length=30, required=False)
    
class CambiarEstadoFlujoForm(forms.Form):
    estado = forms.BooleanField(required=False)
    
class NotasUSForm(forms.Form):
    nombre = forms.CharField(max_length=25)
    descripcion = forms.CharField(max_length=50, required=False) 
    
    def clean_nombre(self):
        """Comprueba que no exista un nombre igual en la db"""
        nombre = self.cleaned_data['nombre']
        if Nota.objects.filter(nombre=nombre):
            raise forms.ValidationError('Nombre de nota ya registrado.')
        return nombre
    
class CambiarEstadoUSFlujoForm(forms.Form):
    estado = forms.IntegerField(required=False)
    actividad_id = forms.IntegerField(required=False)