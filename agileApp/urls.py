# -*- encoding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^usuarios/registro/$', views.registrar_usuarios, name='registrar_usuarios'),
    url(r'^usuarios/index/$', views.index_usuarios, name='index_usuarios'),
    url(r'^usuarios/(?P<user_id>\d+)/editar/$', views.editar_usuarios, name='editar_usuarios'),
    url(r'^usuarios/(?P<user_id>\d+)/eliminar/$', views.eliminar_usuarios, name='eliminar_usuarios'),
    url(r'^usuarios/(?P<user_id>\d+)/delete/$', views.delete_usuarios, name='delete_usuarios'),
    url(r'^usuarios/(?P<user_id>\d+)/ver/$', views.ver_usuarios, name='ver_usuarios'),
]