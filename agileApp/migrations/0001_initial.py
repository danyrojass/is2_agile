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
            name='Actividades',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(default=b'', max_length=20)),
                ('descripcion', models.CharField(default=b'', max_length=30)),
                ('estado', models.IntegerField(default=0)),
                ('numero', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Actividades_Flujos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('actividad', models.ForeignKey(to='agileApp.Actividades')),
            ],
        ),
        migrations.CreateModel(
            name='Flujos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=30, null=True)),
                ('descripcion', models.CharField(default=b'', max_length=50)),
                ('estado', models.BooleanField(default=True)),
                ('actividades', models.ManyToManyField(to='agileApp.Actividades', through='agileApp.Actividades_Flujos')),
            ],
        ),
        migrations.CreateModel(
            name='Flujos_Proyectos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('flujo', models.ForeignKey(to='agileApp.Flujos')),
            ],
        ),
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
                ('flujos', models.ManyToManyField(to='agileApp.Flujos', through='agileApp.Flujos_Proyectos')),
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
            name='Roles_Usuarios_Proyectos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('proyecto', models.ForeignKey(to='agileApp.Proyectos', null=True)),
                ('roles', models.ForeignKey(to='agileApp.Roles')),
            ],
        ),
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(default=b'', max_length=25)),
                ('duracion', models.IntegerField(default=0)),
                ('estado', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Sprint_Proyectos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('proyecto', models.ForeignKey(to='agileApp.Proyectos')),
                ('sprint', models.ForeignKey(to='agileApp.Sprint')),
            ],
        ),
        migrations.CreateModel(
            name='Tipo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='us_Actividades',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('actividad', models.ForeignKey(to='agileApp.Actividades')),
            ],
        ),
        migrations.CreateModel(
            name='us_Flujos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('flujo', models.ForeignKey(to='agileApp.Flujos')),
            ],
        ),
        migrations.CreateModel(
            name='US_Proyectos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('proyecto', models.ForeignKey(to='agileApp.Proyectos')),
            ],
        ),
        migrations.CreateModel(
            name='US_Sprint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sprint', models.ForeignKey(to='agileApp.Sprint')),
            ],
        ),
        migrations.CreateModel(
            name='User_Story',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=50, null=True)),
                ('descripcion', models.CharField(max_length=50, null=True)),
                ('nivel_prioridad', models.IntegerField(null=True)),
                ('valor_negocios', models.IntegerField(null=True)),
                ('valor_tecnico', models.IntegerField(null=True)),
                ('size', models.IntegerField(null=True)),
                ('tiempo_estimado', models.IntegerField(default=0)),
                ('tiempo_real', models.IntegerField(default=0)),
                ('estado', models.IntegerField(default=1)),
                ('fecha_creacion', models.DateField(null=True)),
                ('fecha_inicio', models.DateField(null=True)),
                ('id_flujo', models.IntegerField(null=True)),
                ('id_sprint', models.IntegerField(null=True)),
                ('f_estado', models.IntegerField(null=True)),
                ('f_actividad', models.IntegerField(null=True)),
                ('tipo', models.OneToOneField(null=True, to='agileApp.Tipo')),
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
                ('horas_por_dia', models.IntegerField(null=True)),
                ('roles', models.ManyToManyField(to='agileApp.Roles', through='agileApp.Roles_Usuarios_Proyectos')),
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
            model_name='user_story',
            name='usuario_asignado',
            field=models.OneToOneField(null=True, to='agileApp.Usuarios'),
        ),
        migrations.AddField(
            model_name='us_sprint',
            name='user_story',
            field=models.ForeignKey(to='agileApp.User_Story'),
        ),
        migrations.AddField(
            model_name='us_proyectos',
            name='user_story',
            field=models.ForeignKey(to='agileApp.User_Story'),
        ),
        migrations.AddField(
            model_name='us_flujos',
            name='us',
            field=models.ForeignKey(to='agileApp.User_Story'),
        ),
        migrations.AddField(
            model_name='us_actividades',
            name='us',
            field=models.ForeignKey(to='agileApp.User_Story'),
        ),
        migrations.AddField(
            model_name='sprint',
            name='listaUS',
            field=models.ManyToManyField(to='agileApp.User_Story', through='agileApp.US_Sprint'),
        ),
        migrations.AddField(
            model_name='roles_usuarios_proyectos',
            name='usuarios',
            field=models.ForeignKey(to='agileApp.Usuarios'),
        ),
        migrations.AddField(
            model_name='proyectos',
            name='sprint',
            field=models.ManyToManyField(to='agileApp.Sprint', through='agileApp.Sprint_Proyectos'),
        ),
        migrations.AddField(
            model_name='proyectos',
            name='user_stories',
            field=models.ManyToManyField(to='agileApp.User_Story', through='agileApp.US_Proyectos'),
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
        migrations.AddField(
            model_name='flujos_proyectos',
            name='proyecto',
            field=models.ForeignKey(to='agileApp.Proyectos'),
        ),
        migrations.AddField(
            model_name='flujos',
            name='tipo',
            field=models.OneToOneField(null=True, to='agileApp.Tipo'),
        ),
        migrations.AddField(
            model_name='flujos',
            name='us',
            field=models.ManyToManyField(to='agileApp.User_Story', through='agileApp.us_Flujos'),
        ),
        migrations.AddField(
            model_name='actividades_flujos',
            name='flujo',
            field=models.ForeignKey(to='agileApp.Flujos'),
        ),
        migrations.AddField(
            model_name='actividades',
            name='us',
            field=models.ManyToManyField(to='agileApp.User_Story', through='agileApp.us_Actividades'),
        ),
    ]
