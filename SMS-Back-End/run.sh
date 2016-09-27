#!/usr/bin/env bash
#Fichero de arranque del backend al completo api gateway y el resto de microservicios.
#Ejecución:  . SMS-Back-End/run.sh  estando en la carpeta raíz del proyecto.

# Añadir la detección del directorio google_appengine y en caso de no exisitir decir que se ejecute el requirements

#Mensajes por pantalla
echo -e "\033[32m \n  ### SMS, un proyecto de \033[35m ButterFlyDevs \033[32m ### \033[0m"
echo -e "\033[32m \n  >> Arrancando el BackEnd en local. \033[32m \033[0m"

echo -e "\033[36m \n  Levantando mservicio API Gateway en el puerto 8001\033[0m"
echo -e "\033[36m  Levantando mservicio SBD (Base de Datos) en el puerto 8002\033[0m"
echo -e "\033[36m  Levantando mservicio SCE (Control de Estudiantes) en el puerto 8003\033[0m"

echo -e "\033[36m  Servidor de Administración corriendo en el puerto 8082 (http://localhost:8082) \033[0m"

echo -e "\033[32m \n  ¡Gracias por contribuir! \n\n \033[0m"

#Ejecución del comando que levanta el dev_appserver

../google_appengine/dev_appserver.py \
--port=8001 --admin_port=8082 apigms/apigms.yaml dbms/dbms.yaml sce/sce.yaml
