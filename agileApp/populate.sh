#!/bin/bash

if [ "$1" -eq "1" ]; then
	source ../agileEnv/bin/activate
	python ../manage.py populate_db
	python ../manage.py runserver
	deactivate
else
	python ../manage.py populate_db

fi
