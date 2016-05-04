#Fichero de arranque del front end con la aplicación en AngularJS
#Ejecución:  . SMS-Front-End/run.sh  estando en la carpeta raíz del proyecto.

#Mensajes por pantalla
echo -e "\033[32m \n  ### SMS, un proyecto de \033[35m ButterFlyDevs \033[32m ### \033[0m"
echo -e "\033[32m \n  >> Arrancando el FrontEnd en local. \033[32m \033[0m"

echo -e "\033[36m \n  Levantando aplicación web en el puerto 8080\033[0m"

echo -e "\033[36m  Ya puede acceder desde su navegador en  (http://localhost:8080) \033[0m"

echo -e "\033[32m \n  ¡Gracias por contribuir! \n\n \033[0m"


python google_appengine/dev_appserver.py SMS-Front-End/
