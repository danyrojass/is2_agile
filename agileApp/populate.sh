#!/bin/bash
echo "Por favor, ingrese el número de la opción que desee."
echo "1. Desplegar ambiente de desarrollo. Generar población para la base de datos."
echo "2. Desplegar ambiente de producción. Generar población para la base de datos."
echo "3. Desplegar ambiente de desarrollo."
echo "4. Desplegar ambiente de producción."

read ambiente

echo "Por favor, ingrese el nombre del Tag."

read nombreTag
	
	git checkout $nombreTag;

	if [ "$ambiente" -eq "1" ]; then
		source ../agileEnv/bin/activate
		python ../manage.py populate_db
		python ../manage.py runserver
		deactivate

	elif [ "$ambiente" -eq "2" ]; then
		python ../manage.py populate_db
		echo laluzdelsol | sudo -S command
		mkdir /home/dany/AmbienteProduccion
		cp -a  /home/dany/agile /home/dany/AmbienteProduccion
		sudo chown :www-data /home/dany/AmbienteProduccion
		sudo a2ensite agile.conf
		sudo service apache2 restart

	elif [ "$ambiente" -eq "3" ]; then
		source ../agileEnv/bin/activate
		python ../manage.py runserver
		deactivate

	elif [ "$ambiente" -eq "4" ]; then
		echo laluzdelsol | sudo -S command
		mkdir /home/dany/AmbienteProduccion
		cp -a  /home/dany/agile /home/dany/AmbienteProduccion
		sudo chown :www-data /home/dany/AmbienteProduccion
		sudo a2ensite agile.conf
		sudo service apache2 restart
	fi
