# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Permisos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(default=b'', max_length=50)),
                ('nivel', models.IntegerField()),
                ('estado', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Permisos_Roles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('permisos', models.ForeignKey(to='agileApp.Permisos')),
            ],
        ),
        migrations.CreateModel(
            name='Proyectos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre_largo', models.CharField(default=b'', max_length=25)),
                ('nombre_corto', models.CharField(default=b'', max_length=10)),
                ('tipo', models.BooleanField(default=True)),
                ('descripcion', models.CharField(default=b'', max_length=50)),
                ('fecha_inicio', models.DateField(default=django.utils.timezone.now)),
                ('fecha_fin_estimado', models.DateField(default=django.utils.timezone.now)),
                ('fecha_fin_real', models.DateField(default=django.utils.timezone.now)),
                ('observaciones', models.CharField(default=b'', max_length=50)),
                ('estado', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(default=b'', max_length=25)),
                ('tipo', models.BooleanField(default=False)),
                ('estado', models.BooleanField(default=False)),
                ('observacion', models.CharField(default=b'', max_length=50)),
                ('permisos', models.ManyToManyField(to='agileApp.Permisos', through='agileApp.Permisos_Roles')),
            ],
        ),
        migrations.CreateModel(
            name='Roles_Usuarios',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('roles', models.ForeignKey(to='agileApp.Roles')),
            ],
        ),
        migrations.CreateModel(
            name='Roles_Usuarios_Proyectos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('proyecto', models.ForeignKey(to='agileApp.Proyectos')),
                ('roles', models.ForeignKey(to='agileApp.Roles')),
            ],
        ),
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('telefono', models.CharField(default=b'', max_length=15)),
                ('direccion', models.CharField(default=b'', max_length=45)),
                ('tipo', models.CharField(default=b'', max_length=10)),
                ('observacion', models.CharField(default=b'', max_length=50)),
                ('roles', models.ManyToManyField(to='agileApp.Roles', through='agileApp.Roles_Usuarios')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Usuarios_Proyectos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('proyecto', models.ForeignKey(to='agileApp.Proyectos')),
                ('usuarios', models.ForeignKey(to='agileApp.Usuarios')),
            ],
        ),
        migrations.AddField(
            model_name='roles_usuarios_proyectos',
            name='usuarios',
            field=models.ForeignKey(to='agileApp.Usuarios'),
        ),
        migrations.AddField(
            model_name='roles_usuarios',
            name='usuario',
            field=models.ForeignKey(to='agileApp.Usuarios'),
        ),
        migrations.AddField(
            model_name='proyectos',
            name='usuarios',
            field=models.ManyToManyField(to='agileApp.Usuarios', through='agileApp.Usuarios_Proyectos'),
        ),
        migrations.AddField(
            model_name='permisos_roles',
            name='roles',
            field=models.ForeignKey(to='agileApp.Roles'),
        ),
    ]
