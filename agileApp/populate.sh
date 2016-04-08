#!/bin/bash

if [ "$#" -eq "2" ]; then
	re='^[0-9]+$'
	if ! [[ $1 =~ $re ]] ; then
  		echo "El primer parámetro no es un número." >&2;
	else
		nombreTag=$2
		
		git checkout $nombreTag;

		if [ "$1" -eq "1" ]; then
			source ../agileEnv/bin/activate
			python ../manage.py populate_db
			python ../manage.py runserver
			deactivate

		elif [ "$1" -eq "2" ]; then
			python ../manage.py populate_db
			firefox 0.0.0.0

		elif [ "$1" -eq "3" ]; then
			source ../agileEnv/bin/activate
			python ../manage.py runserver
			deactivate

		elif [ "$1" -eq "4" ]; then
			firefox 0.0.0.0
		fi
	fi

else
	echo "La cantidad de parámetros es diferente a dos (2).";
fi
