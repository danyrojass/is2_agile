#!/bin/bash
echo "Por favor, ingrese el número de la opción que desee."
echo "1. Desplegar ambiente de desarrollo. Generar población para la base de datos."
echo "2. Desplegar ambiente de producción. Generar población para la base de datos."
echo "3. Desplegar ambiente de desarrollo."
echo "4. Desplegar ambiente de producción."

read ambiente

echo "Por favor, elija si quiere descargar en forma remota o local."
echo "1. Remota."
echo "2. Local."

read opcion

echo "Por favor, ingrese el nombre del Tag."

read nombreTag
	
	if [ "$ambiente" -eq "1" ] || [ "$ambiente" -eq 3 ] ; then
		sudo -u postgres -H -- psql -c "DROP DATABASE agile_desarrollo;"
		echo "Base de datos elminada."
		sudo -u postgres -H -- psql -c "CREATE DATABASE agile_desarrollo WITH OWNER agile;"
		sudo -u postgres -H -- psql -c "GRANT ALL PRIVILEGES ON DATABASE agile_desarrollo TO agile;"
		echo "Base de datos creada."
	elif [ "$ambiente" -eq "2" ] || [ "$ambiente" -eq 4 ]; then
		sudo -u postgres -H -- psql -c "DROP DATABASE agile_produccion;"
		echo "Base de datos elminada."
		sudo -u postgres -H -- psql -c "CREATE DATABASE agile_produccion WITH OWNER agile;"
		sudo -u postgres -H -- psql -c "GRANT ALL PRIVILEGES ON DATABASE agile_produccion TO agile;"
		echo "Base de datos creada."
	fi
	
	if [ "$ambiente" -eq "1" ]; then
		rm -r /home/dany/AmbienteDesarrollo
		mkdir /home/dany/AmbienteDesarrollo
		cd /home/dany/AmbienteDesarrollo
		if [ "$opcion" -eq "1" ]; then
			git clone -b $nombreTag --single-branch --depth 1 https://github.com/danyrojass/is2_agile.git
			cd /home/dany/AmbienteDesarrollo/is2_agile
		elif [ "$opcion" -eq "2" ]; then
			git clone -b $nombreTag /home/dany/agile/.git
			cd /home/dany/AmbienteDesarrollo/agile
		fi
		source agileEnv/bin/activate
		python manage.py createsuperuser --username=agile --email=agile@example.com
		echo "Ingresar la contraseña para el súper usuario: "
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
			git clone -b $nombreTag --single-branch --depth 1 https://github.com/danyrojass/is2_agile.git
			cd /home/dany/AmbienteProduccion/is2_agile
		elif [ "$opcion" -eq "2" ]; then
			git clone -b $nombreTag /home/dany/agile/.git
			cd /home/dany/AmbienteProduccion/agile
		fi
		python manage.py createsuperuser --username=agile --email=agile@example.com
		echo "Ingresar la contraseña para el súper usuario: "
		python manage.py makemigrations
		python manage.py migrate
		pyton manage.py populate_db
		python manage.py collectstatic
		sudo chown :www-data /home/dany/AmbienteProduccion
		sudo a2ensite agile.conf
		sudo service apache2 restart

	elif [ "$ambiente" -eq "3" ]; then
		sudo rm -r /home/dany/AmbienteDesarrollo
		mkdir /home/dany/AmbienteDesarrollo
		cd /home/dany/AmbienteDesarrollo
		if [ "$opcion" -eq "1" ]; then
			git clone -b $nombreTag --single-branch --depth 1 https://github.com/danyrojass/is2_agile.git
			cd /home/dany/AmbienteDesarrollo/is2_agile
		elif [ "$opcion" -eq "2" ]; then
			git clone -b $nombreTag /home/dany/agile/.git
			cd /home/dany/AmbienteDesarrollo/agile
		fi
		source agileEnv/bin/activate
		python manage.py createsuperuser --username=agile --email=agile@example.com
		echo "Ingresar la contraseña para el súper usuario: "
		python manage.py makemigrations
		python manage.py migrate
		python manage.py runserver
		deactivate

	elif [ "$ambiente" -eq "4" ]; then
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
		python manage.py createsuperuser --username=agile --email=agile@example.com
		echo "Ingresar la contraseña para el súper usuario: "
		python manage.py makemigrations
		python manage.py migrate
		python manage.py collectstatic
		sudo chown :www-data /home/dany/AmbienteProduccion
		sudo a2ensite agile.conf
		sudo service apache2 restart

	fi
