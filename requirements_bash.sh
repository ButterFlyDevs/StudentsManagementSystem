echo -e "\033[32m \n\t ### SMS, un proyecto de \033[35m ButterFlyDevs \033[32m ### \033[0m"
echo -e "\033[32m \n\t Gracias por contribuir \033[0m"

echo "Preparando el entorno..."

#Descargado el SDK de GAE

echo -e "\n\033[32m 0.1 Instalando unzip \033[0m\n"
sudo apt-get install unzip
echo -e "\n\033[32m 0.2 Instalando curl \033[0m\n"
sudo apt-get install curl
echo -e "\n\033[31m 1. Descargando el SDK de Google App Engine \033[0m\n"
curl -O https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.30.zip
echo "Unzip SDK"
unzip google_appengine_1.9.30.zip
echo "Deleting .zip"
rm google_appengine_1.9.30.zip


#Instalación de MySQL de forma desatendida.

echo -e "\n\033[31m 2. Instalando MySQL de forma desatendida \033[0m\n"

sudo apt-get update
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password root'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password root'
sudo apt-get --force-yes -y install mysql-server

#Esto elimina todos los paquetes de mysql
#sudo apt-get remove --purge mysql*
#sudo apt-get autoremove
#sudo apt-get autoclean

echo -e "\033[31m"
echo "Instalación MySQL finalizada:"
mysql --version
echo "Arrancando el demonio:"
sudo /etc/init.d/mysql start
echo -e "\033[0m"

#Instalamos la librería de python
echo -e "\n\033[31m 3. Instalando la librería de python para mysql \033[0m\n"
sudo apt-get install python-mysqldb

#Instalando el gestor de paquetes de python.
echo -e "\n\033[31m 4. Instaladon el gestor de paquetes de python \033[0m\n"
sudo apt-get install python-pip

#Ayuda:
echo "Si alguno de los paquetes no se ha instalado correctamente por favor inténtelo manualmente. Para conocer más
información lea el fichero contributing.md, la sección [Entorno de desarrollo]."
