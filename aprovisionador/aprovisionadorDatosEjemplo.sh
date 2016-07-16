#!/bin/bash

#Fichero que aprovisiona el sistema con datos de muestra para comprobar su funcionamiento y extender funcionalidad.
#Atención, este fichero deberá ser modificado cuando se modifique algo en el sistema para que no pierda funcionalidad.

##### Aprovisionador que sólo hace uso de la APIG para su interacción con el sistema, como lo haría la
##### interfaz gráfica con el backend. Debe ejecutarse tras el lanzamiento de runAll.sh

cat << "EOF"
 ▄▄▄▄▄▄▄▄▄▄▄  ▄▄       ▄▄  ▄▄▄▄▄▄▄▄▄▄▄
▐░░░░░░░░░░░▌▐░░▌     ▐░░▌▐░░░░░░░░░░░▌
▐░█▀▀▀▀▀▀▀▀▀ ▐░▌░▌   ▐░▐░▌▐░█▀▀▀▀▀▀▀▀▀
▐░█▄▄▄▄▄▄▄▄▄ ▐░▌ ▐░▐░▌ ▐░▌▐░█▄▄▄▄▄▄▄▄▄
▐░░░░░░░░░░░▌▐░▌  ▐░▌  ▐░▌▐░░░░░░░░░░░▌
 ▀▀▀▀▀▀▀▀▀█░▌▐░▌   ▀   ▐░▌ ▀▀▀▀▀▀▀▀▀█░▌
 ▄▄▄▄▄▄▄▄▄█░▌▐░▌       ▐░▌ ▄▄▄▄▄▄▄▄▄█░▌
▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌
 ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀
EOF
echo -e "\n### Aprovisionador de datos de muestra del sistema ###\n"

echo -e "\n### Reseteando Base de Datos en microSBD ###\n"
mysql -u root -p'root' < ../SMS-Back-End/sbd/APIDB/DBCreatorv1.sql

sleep 1

################################
#### Insercción de 6 alumnos ###
################################

# Insertamos el Alumno A
rep=$(curl -H "Content-Type: application/json" -d @bobEsponja.json -X POST   localhost:8001/_ah/api/helloworld/v1/entidades)

echo ${rep}

#echo ${rep} | jq '.status'

var=echo "$rep" | jq '.status'

echo $status
echo $?
# Insertamos la imagen para el alumno A
#curl -d "nombre=prueba" --data-urlencode 'imagen='"$( base64 bobEsponja.jpg)"''  -X POST -G localhost:8001/_ah/api/helloworld/v1/imagenes/subirImagen
# Asociamos esa imagen al alumno A
