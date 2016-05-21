# -*- encoding: utf-8 -*-
from django.conf.urls import url

from . import views
 
urlpatterns = [
    url(r'^usuarios/registro/$', views.registrar_usuarios, name='registrar_usuarios'),
    url(r'^usuarios/modificar_contrasena/$', views.modificar_contrasena, name='modificar_contrasena'),
    url(r'^usuarios/index/$', views.index_usuarios, name='index_usuarios'),
    url(r'^usuarios/(?P<user_id>\d+)/editar/$', views.editar_usuarios, name='editar_usuarios'),
    url(r'^usuarios/(?P<user_id>\d+)/eliminar/$', views.eliminar_usuarios, name='eliminar_usuarios'),
    url(r'^usuarios/(?P<user_id>\d+)/delete/$', views.delete_usuarios, name='delete_usuarios'),
    url(r'^usuarios/(?P<user_id>\d+)/ver/$', views.ver_usuarios, name='ver_usuarios'),
    url(r'^roles/crear/$', views.crear_roles, name='crear_roles'),
    url(r'^roles/index/$', views.index_roles, name='index_roles'),
    url(r'^roles/(?P<rol_id>\d+)/editar/$', views.editar_roles, name='editar_roles'),
    url(r'^roles/(?P<rol_id>\d+)/ver/$', views.ver_roles, name='ver_roles'),
    url(r'^roles/(?P<rol_id>\d+)/eliminar/$', views.eliminar_roles, name='eliminar_roles'),
    url(r'^roles/(?P<rol_id>\d+)/delete/$', views.delete_roles, name='delete_roles'),
    url(r'^proyectos/crear/$', views.crear_proyectos, name='crear_proyectos'),
    url(r'^proyectos/(?P<proyecto_id>\d+)/editar/$', views.editar_proyectos, name='editar_proyectos'),
    url(r'^proyectos/(?P<proyecto_id>\d+)/ver/$', views.ver_proyectos, name='ver_proyectos'),
    url(r'^proyectos/index/$', views.index_proyectos, name='index_proyectos'),
    url(r'^usuario/(?P<user_id>\d+)/proyecto/(?P<proyecto_id>\d+)/index$', views.index_ususario_proyecto, name='index_ususario_proyecto'),
    url(r'^usuario/(?P<user_id>\d+)/proyecto/(?P<proyecto_id>\d+)/proyecto$', views.index_proyecto_usuario, name='index_proyecto_usuario'),
    url(r'^usuario/(?P<user_id>\d+)/proyecto/(?P<proyecto_id>\d+)/definir/$', views.definir_proyectos, name='definir_proyectos'),
    url(r'^usuario/(?P<user_id>\d+)/proyecto/(?P<proyecto_id>\d+)/desasignar/(?P<userd_id>\d+)/$', views.eliminar_usuario_proyecto, name='eliminar_usuario_proyecto'),
    url(r'^usuario/(?P<user_id>\d+)/proyecto/(?P<proyecto_id>\d+)/asignar/$', views.asignar_roles_usuarios_proyecto, name='asignar_roles_usuarios_proyecto'),
    url(r'^usuario/(?P<user_id>\d+)/proyecto/(?P<proyecto_id>\d+)/crear_us/$', views.crear_us, name='crear_us'),
    url(r'^usuario/(?P<user_id>\d+)/proyecto/(?P<proyecto_id>\d+)/index_us/$', views.index_us, name='index_us'), 
    url(r'^usuario/(?P<user_id>\d+)/proyecto/(?P<proyecto_id>\d+)/us/(?P<us_id>\d+)/modificar$', views.modificar_us, name='modificar_us'),
    url(r'^usuario/(?P<user_id>\d+)/proyecto/(?P<proyecto_id>\d+)/us/(?P<us_id>\d+)/asignar', views.asignar_us, name='asignar_us'),
    url(r'^usuario/(?P<user_id>\d+)/proyecto/(?P<proyecto_id>\d+)/us/(?P<us_id>\d+)/ver/', views.ver_us, name='ver_us'),
    url(r'^usuario/(?P<user_id>\d+)/proyecto/(?P<proyecto_id>\d+)/us/(?P<us_id>\d+)/cambiar_estado/', views.cambiar_estado_us, name='cambiar_estado_us'),
    url(r'^usuario/(?P<user_id>\d+)/proyecto/(?P<proyecto_id>\d+)/index_sprints/$', views.index_sprint, name='index_sprint'),
    url(r'^usuario/(?P<user_id>\d+)/proyecto/(?P<proyecto_id>\d+)/crear_sprint/', views.crear_sprint, name='crear_sprint'),
    url(r'^usuario/(?P<user_id>\d+)/proyecto/(?P<proyecto_id>\d+)/sprint/(?P<sp_id>\d+)/modificar/', views.modificar_sprint, name='modificar_sprint'),
    url(r'^usuario/(?P<user_id>\d+)/proyecto/(?P<proyecto_id>\d+)/sprint/(?P<sp_id>\d+)/ver/', views.ver_sprint, name='ver_sprint'),
    url(r'^usuario/(?P<user_id>\d+)/proyecto/(?P<proyecto_id>\d+)/sprint/(?P<sp_id>\d+)/asignar_US/', views.asignar_us_sprint, name='asignar_us_sprint'),
    url(r'^usuario/(?P<user_id>\d+)/proyecto/(?P<proyecto_id>\d+)/sprint/(?P<sp_id>\d+)/cambiar_estado/', views.cambiar_estado_sprint, name='cambiar_estado_sprint'),
    url(r'^usuario/(?P<user_id>\d+)/proyecto/(?P<proyecto_id>\d+)/index_flujo/$', views.index_flujo, name='index_flujo'), 
    url(r'^usuario/(?P<user_id>\d+)/proyecto/(?P<proyecto_id>\d+)/crear_flujo/$', views.crear_flujo, name='crear_flujo'), 
    url(r'^usuario/(?P<user_id>\d+)/proyecto/(?P<proyecto_id>\d+)/flujo/(?P<flujo_id>\d+)/crear_actividad/$', views.crear_actividad, name='crear_actividad'), 
    url(r'^usuario/(?P<user_id>\d+)/proyecto/(?P<proyecto_id>\d+)/flujo/(?P<flujo_id>\d+)/visualizar_flujo/$', views.visualizar_flujo, name='visualizar_flujo'), 
    url(r'^usuario/(?P<user_id>\d+)/proyecto/(?P<proyecto_id>\d+)/flujo/(?P<flujo_id>\d+)/modificar_flujo/$', views.modificar_flujo, name='modificar_flujo'), 
    url(r'^usuario/(?P<user_id>\d+)/proyecto/(?P<proyecto_id>\d+)/flujo/(?P<flujo_id>\d+)/cambiar_estado/$', views.cambiar_estado_flujo, name='cambiar_estado_flujo'), 
    url(r'^usuario/(?P<user_id>\d+)/proyecto/(?P<proyecto_id>\d+)/flujo/(?P<flujo_id>\d+)/asignar_flujo/$', views.asignar_flujo, name='asignar_flujo'),  
    url(r'^usuario/(?P<user_id>\d+)/proyecto/(?P<proyecto_id>\d+)/flujo/(?P<flujo_id>\d+)/actividad/(?P<actividad_id>\d+)/modificar_actividad/$', views.modificar_actividad, name='modificar_actividad'), 
    url(r'^usuario/(?P<user_id>\d+)/proyecto/(?P<proyecto_id>\d+)/flujo/(?P<flujo_id>\d+)/visualizar_kanban/$', views.visualizar_kanban, name='visualizar_kanban'), 
    url(r'^usuario/(?P<user_id>\d+)/proyecto/(?P<proyecto_id>\d+)/flujo/(?P<flujo_id>\d+)/cambiar_estado_kanban/(?P<us_id>\d+)/$', views.cambiar_estado_kanban, name='cambiar_estado_kanban'), 
    
]