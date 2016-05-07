from django.contrib import admin

# Register your models here.
from .models import Usuarios, Permisos, Roles, Proyectos, Permisos_Roles, Roles_Usuarios_Proyectos,\
Roles_Usuarios, Usuarios_Proyectos, User_Story, US_Proyectos, Flujos

admin.site.register(Usuarios)
admin.site.register(Permisos)
admin.site.register(Roles)
admin.site.register(Proyectos)
admin.site.register(Permisos_Roles)
admin.site.register(Roles_Usuarios)
admin.site.register(Usuarios_Proyectos)
admin.site.register(Roles_Usuarios_Proyectos)
admin.site.register(User_Story)
admin.site.register(US_Proyectos)
admin.site.register(Flujos)