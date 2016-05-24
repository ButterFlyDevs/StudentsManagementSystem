echo -e "\033[32m \n\t ### SMS, un proyecto de \033[35m ButterFlyDevs \033[32m ### \033[0m"
echo -e "\033[32m \n\t Gracias por contribuir \033[0m"

echo "COMENZANDO ELIMINACION."

#Descargado el SDK de GAE

echo -e "\n\033[32m 0.1 Desinstalando unzip \033[0m\n"
sudo apt-get --purge -y remove unzip
echo -e "\n\033[32m 0.2 Desinstalando curl \033[0m\n"
sudo apt-get --purge -y remove curl



#Desinstalación de MySQL de forma desatendida.

echo -e "\n\033[31m 2. Desinstalando MySQL de forma desatendida \033[0m\n"

sudo apt-get update
#sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password root'
#sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password root'
sudo apt-get --purge -y mysql*


#Esto elimina todos los paquetes de mysql
#sudo apt-get remove --purge mysql*
#sudo apt-get autoremove
#sudo apt-get autoclean

echo -e "\033[31m"
echo "Desinstalación MySQL finalizada:"
#mysql --version

#Instalamos la librería de python
echo -e "\n\033[31m 3. Desinstalando la librería de python para mysql \033[0m\n"
sudo apt-get --purge -y remove python-mysqldb

#Instalando el gestor de paquetes de python.
echo -e "\n\033[31m 4. Instaladon el gestor de paquetes de python \033[0m\n"
sudo apt-get --purge -y remove python-pip

#Eliminando librerias de Pytrhon de los microservicios

rm -rf SMS-Back-End/microservicio1/lib/
rm -rf SMS-Back-End/microservicio2/lib/
rm -rf SMS-Back-End/sce/lib/
#Ayuda:
echo "Si alguno de los paquetes no se ha instalado correctamente por favor inténtelo manualmente. Para conocer más
información lea el fichero contributing.md, la sección [Entorno de desarrollo]."
