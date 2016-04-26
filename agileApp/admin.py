from django.contrib import admin

# Register your models here.
from .models import Usuarios, Permisos, Roles, Proyectos, Permisos_Roles, Roles_Usuarios, Usuarios_Proyectos

admin.site.register(Usuarios)
admin.site.register(Permisos)
admin.site.register(Roles)
admin.site.register(Proyectos)
admin.site.register(Permisos_Roles)
admin.site.register(Roles_Usuarios)
admin.site.register(Usuarios_Proyectos)