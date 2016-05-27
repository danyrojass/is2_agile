#!/bin/bash
echo "Por favor, ingrese el número de la opción que desee."
echo "1. Desplegar ambiente de desarrollo. Generar población para la base de datos."
echo "2. Desplegar ambiente de producción. Generar población para la base de datos."

read ambiente

echo "Por favor, elija si quiere descargar en forma remota o local."
echo "1. Remota."
echo "2. Local."

read opcion

echo "Por favor, ingrese el nombre del Tag."
echo "V4: Tag Nro. 4."

read nombreTag
	sudo service postgresql restart 
	if [ "$ambiente" -eq "1" ] ; then
		sudo -u postgres -- psql -c "DROP DATABASE agile_desarrollo;"
		echo "Base de datos elminada."
		sudo -u postgres -- psql -c "CREATE DATABASE agile_desarrollo WITH OWNER agile;"
		sudo -u postgres -- psql -c "GRANT ALL PRIVILEGES ON DATABASE agile_desarrollo TO agile;"
		echo "Base de datos creada."
		
	elif [ "$ambiente" -eq "2" ]; then
		sudo -u postgres -- psql -c "DROP DATABASE agile_produccion;"
		echo "Base de datos elminada."
		sudo -u postgres -- psql -c "CREATE DATABASE agile_produccion WITH OWNER agile;"
		sudo -u postgres -- psql -c "GRANT ALL PRIVILEGES ON DATABASE agile_produccion TO agile;"
		echo "Base de datos creada."
	fi
	
	if [ "$ambiente" -eq "1" ]; then
		sudo rm -r /home/dany/AmbienteDesarrollo
		mkdir /home/dany/AmbienteDesarrollo
		cd /home/dany/AmbienteDesarrollo
		if [ "$opcion" -eq "1" ]; then
			git clone -b $nombreTag https://github.com/danyrojass/is2_agile.git
			cd /home/dany/AmbienteDesarrollo/is2_agile
			
			rm -r /home/dany/AmbienteDesarrollo/is2_agile/agileApp/migrations/__init__.pyc
			rm -r /home/dany/AmbienteDesarrollo/is2_agile/agileApp/migrations/0001_initial.py
			rm -r /home/dany/AmbienteDesarrollo/is2_agile/agileApp/migrations/0001_initial.pyc			

			sed  -i  's/VIRTUAL_ENV="\/home\/dany\/agile\/agileEnv"/VIRTUAL_ENV="\/home\/dany\/AmbienteDesarrollo\/agile\/agileEnv"/g' /home/dany/AmbienteDesarrollo/is2_agile/agileEnv/bin/activate
			source agileEnv/bin/activate
		elif [ "$opcion" -eq "2" ]; then
			git clone -b $nombreTag /home/dany/agile/.git
			cd /home/dany/AmbienteDesarrollo/agile
			
			rm -r /home/dany/AmbienteDesarrollo/agile/agileApp/migrations/__init__.pyc
			rm -r /home/dany/AmbienteDesarrollo/agile/agileApp/migrations/0001_initial.py
			rm -r /home/dany/AmbienteDesarrollo/agile/agileApp/migrations/0001_initial.pyc			

			sed  -i  's/VIRTUAL_ENV="\/home\/dany\/agile\/agileEnv"/VIRTUAL_ENV="\/home\/dany\/AmbienteDesarrollo\/agile\/agileEnv"/g' /home/dany/AmbienteDesarrollo/agile/agileEnv/bin/activate
			source agileEnv/bin/activate
		fi
					
		python manage.py syncdb
		python manage.py makemigrations
		python manage.py migrate
		python manage.py populate_db
		
		python manage.py runserver
		deactivate

	elif [ "$ambiente" -eq "2" ]; then
		sudo rm -r /home/dany/AmbienteProduccion
		mkdir /home/dany/AmbienteProduccion
		cd /home/dany/AmbienteProduccion
		if [ "$opcion" -eq "1" ]; then
			git clone -b $nombreTag https://github.com/danyrojass/is2_agile.git
			cd /home/dany/AmbienteProduccion/is2_agile

			rm -r /home/dany/AmbienteProduccion/is2_agile/agileApp/migrations/__init__.pyc
			rm -r /home/dany/AmbienteProduccion/is2_agile/agileApp/migrations/0001_initial.py
			rm -r /home/dany/AmbienteProduccion/is2_agile/agileApp/migrations/0001_initial.pyc				

		elif [ "$opcion" -eq "2" ]; then
			git clone -b $nombreTag /home/dany/agile/.git
			cd /home/dany/AmbienteProduccion/agile

			rm -r /home/dany/AmbienteProduccion/agile/agileApp/migrations/__init__.pyc
			rm -r /home/dany/AmbienteProduccion/agile/agileApp/migrations/0001_initial.py
			rm -r /home/dany/AmbienteProduccion/agile/agileApp/migrations/0001_initial.pyc	
		fi
		python manage.py syncdb
		python manage.py makemigrations
		python manage.py migrate
		python manage.py populate_db
		
		python manage.py collectstatic
		sudo chown :www-data /home/dany/AmbienteProduccion/agile
		sudo a2ensite agile.conf
		sudo service apache2 restart
		cd /home/dany/agile/agileApp
	fi
