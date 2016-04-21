# -*- encoding: utf-8 -*-
from django.db import models
from django.conf import settings


class Usuarios(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    telefono = models.CharField(max_length=15, default="")
    direccion = models.CharField(max_length=45, default="")
    tipo = models.CharField(max_length=2, default="")
    observacion = models.CharField(max_length=50, default="")
    #roles = models.ManyToManyField(Roles, through='Roles_Usuarios')
    
    def __str__(self):
        return self.user.username
