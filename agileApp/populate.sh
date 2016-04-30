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
			git clone -b $nombreTag --single-branch --depth 1 https://github.com/danyrojass/is2_agile.git
			cd /home/dany/AmbienteDesarrollo/is2_agile
			sed  -i  's/VIRTUAL_ENV="\/home\/dany\/agile\/agileEnv"/VIRTUAL_ENV="\/home\/dany\/AmbienteDesarrollo\/agile\/agileEnv"/g' /home/dany/AmbienteDesarrollo/is2_agile/agileEnv/bin/activate
			source agileEnv/bin/activate
		elif [ "$opcion" -eq "2" ]; then
			git clone -b $nombreTag /home/dany/agile/.git
			cd /home/dany/AmbienteDesarrollo/agile
			sed  -i  's/VIRTUAL_ENV="\/home\/dany\/agile\/agileEnv"/VIRTUAL_ENV="\/home\/dany\/AmbienteDesarrollo\/agile\/agileEnv"/g' /home/dany/AmbienteDesarrollo/agile/agileEnv/bin/activate
			source agileEnv/bin/activate
		fi
					
		python manage.py syncdb
		python manage.py migrate
		python manage.py populate_db
		python manage.py runserver
		deactivate

	elif [ "$ambiente" -eq "2" ]; then
		sudo rm -r /home/dany/AmbienteProduccion
		mkdir /home/dany/AmbienteProduccion
		cd /home/dany/AmbienteProduccion
		if [ "$opcion" -eq "1" ]; then
			git clone -b $nombreTag --single-branch --depth 1 https://github.com/danyrojass/is2_agile.git
			cd /home/dany/AmbienteProduccion/is2_agile
		elif [ "$opcion" -eq "2" ]; then
			git clone -b $nombreTag /home/dany/agile/.git
			cd /home/dany/AmbienteProduccion/agile
		fi
		python manage.py syncdb
		python manage.py migrate
		pyton manage.py populate_db
		python manage.py collectstatic
		sudo chown :www-data /home/dany/AmbienteProduccion/agile
		sudo a2ensite agile.conf
		sudo service apache2 restart

	fi
