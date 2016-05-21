from django.contrib import admin

# Register your models here.
from .models import Usuarios, Permisos, Roles, Proyectos, Permisos_Roles, Roles_Usuarios_Proyectos,\
Usuarios_Proyectos, User_Story, US_Proyectos, Flujos, Flujos_Proyectos, Actividades_Flujos, Actividades
from agileApp.models import Tipo, us_Flujos

admin.site.register(Usuarios)
admin.site.register(Permisos)
admin.site.register(Roles)
admin.site.register(Proyectos)
admin.site.register(Permisos_Roles)
admin.site.register(Usuarios_Proyectos)
admin.site.register(Roles_Usuarios_Proyectos)
admin.site.register(User_Story)
admin.site.register(US_Proyectos)
admin.site.register(Flujos)
admin.site.register(Flujos_Proyectos)
admin.site.register(Actividades)
admin.site.register(Actividades_Flujos)
admin.site.register(Tipo)
admin.site.register(us_Flujos)

