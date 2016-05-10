#!/bin/bash

#Contamos las lineas del mServicio apigateway
APIG_lines="$(wc -l $(find SMS-Back-End/apigateway/ ! -name *.pyc ! -name *.jpg ! -path 'SMS-Back-End/apigateway/lib/*' ! -wholename SMS-Back-End/apigateway/lib ! -wholename SMS-Back-End/apigateway/) | grep 'total' | awk '{print $1}')"

UI_lines="$(wc -l $(find SMS-Front-End/ ! -name *.pyc ! -name *.jpg ! -path 'SMS-Back-End/apigateway/lib/*' ! -wholename SMS-Back-End/apigateway/lib ! -wholename SMS-Back-End/apigateway/) | grep 'total' | awk '{print $1}')"

#Contamos las lineas del mServicio Base de Datos
mSBD_lines="$(wc -l SMS-Back-End/microservicio1/*.py SMS-Back-End/microservicio1/*.txt SMS-Back-End/microservicio1/*.yaml | grep 'total' | cut -d' ' -f2)"

#Contamos las lineas del mServicio Control Estudiantes
mSCE_lines="$(wc -l SMS-Back-End/sce/*.py SMS-Back-End/sce/*.txt SMS-Back-End/sce/*.yaml | grep 'total' | cut -d' ' -f2)"

#Número del commit:
commit_number="$(git rev-list --count HEAD)"

#Vamos a guardar una linea separándola con ';'
file_line=$commit_number";"$(date +"%d-%m-%Y")";"$APIG_lines";"$mSBD_lines";"$mSCE_lines";"

echo $file_line


#Después realizamos la escritura en un fichero de la rama gh-pages para que se muestre el gráfico en la web.

#git checkout gh-pages

#echo $APIG_lines >> lines.txt

#git commit -am "Prueba de escritura"

#git checkout master
