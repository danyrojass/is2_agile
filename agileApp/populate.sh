#!/bin/bash
echo "Por favor, ingrese el número de la opción que desee."
echo "1. Desplegar ambiente de desarrollo. Generar población para la base de datos."
echo "2. Desplegar ambiente de producción. Generar población para la base de datos."
echo "3. Desplegar ambiente de desarrollo."
echo "4. Desplegar ambiente de producción."

read ambiente

echo "Por favor, ingrese el nombre del Tag."

read nombreTag
	
	

	if [ "$ambiente" -eq "1" ]; then
		rm -r /home/dany/AmbienteDesarrollo
		mkdir /home/dany/AmbienteDesarrollo
		cd /home/dany/AmbienteDesarrollo
		git clone -b $nombreTag --single-branch --depth 1 https://github.com/danyrojass/is2_agile.git
		cd /home/dany/AmbienteDesarrollo/is2_agile
		source agileEnv/bin/activate
		python manage.py populate_db
		python manage.py runserver
		deactivate

	elif [ "$ambiente" -eq "2" ]; then
		rm -r /home/dany/AmbienteProduccion
		mkdir /home/dany/AmbienteProduccion
		cd /home/dany/AmbienteProduccion
		git clone -b $nombreTag --single-branch --depth 1 https://github.com/danyrojass/is2_agile.git
		cd  /home/dany/AmbienteProduccion/is2_agile
		pyton manage.py populate_db
		echo laluzdelsol | sudo -S command
		sudo chown :www-data /home/dany/AmbienteProduccion
		sudo a2ensite agile.conf
		sudo service apache2 restart

	elif [ "$ambiente" -eq "3" ]; then
		rm -r /home/dany/AmbienteDesarrollo
		mkdir /home/dany/AmbienteDesarrollo
		cd /home/dany/AmbienteDesarrollo
		git clone -b $nombreTag --single-branch --depth 1 https://github.com/danyrojass/is2_agile.git
		cd /home/dany/AmbienteDesarrollo/is2_agile
		source agileEnv/bin/activate
		python manage.py runserver
		deactivate

	elif [ "$ambiente" -eq "4" ]; then
		rm -r /home/dany/AmbienteProduccion
		mkdir /home/dany/AmbienteProduccion
		cd /home/dany/AmbienteProduccion
		git clone -b $nombreTag --single-branch --depth 1 https://github.com/danyrojass/is2_agile.git
		cd  /home/dany/AmbienteProduccion/is2_agile
		echo laluzdelsol | sudo -S command
		sudo chown :www-data /home/dany/AmbienteProduccion
		sudo a2ensite agile.conf
		sudo service apache2 restart

	fi
