#!/usr/bin/env bash
echo -e "\033[32m \n\t ### SMS, a project of  \033[35m ButterFlyDevs \033[32m ### \033[0m"
echo -e "\033[32m \n\t Thanks for contributing. \033[0m"


echo -e "It will be installed a lot of required software.\n"


read -p "Are you sure? [y/n]: " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then

    echo -e "\n\033[32m 1. Installing unzip \033[0m\n"
    sudo apt-get install -y unzip

    echo -e "\n\033[32m 2. Installing curl \033[0m\n"
    sudo apt-get install -y curl

    echo -e "\n\033[31m 3. Downloading Google App Engine SDK v.1.9.30 \033[0m\n"
    curl -O https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.30.zip

    echo -e "\n\033[34m 4. Unzip SDK \033[0m\n"
    unzip google_appengine_1.9.30.zip

    echo -e "\n\033[34m 5. Deleting .zip \033[0m\n"
    rm google_appengine_1.9.30.zip


    echo -e "\n\033[31m 6. Instalando MySQL de forma desatendida \033[0m\n"

    sudo apt-get update
    sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password root'
    sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password root'
    sudo apt-get --force-yes -y install mysql-server

    echo -e "\033[31m"
    echo "MySQL installation finished"
    mysql --version


    echo -e "\n\033[31m 7. Installing python mysqldb library \033[0m\n"
    sudo apt-get install -y python-mysqldb

    echo -e "\n\033[31m 8. Installing python PIP packages manager \033[0m\n"
    sudo apt-get install -y python-pip

    echo -e "\n\033[32m ### Dependencies of MICROSERVICES ### \033[0m\n"

    echo -e "\n\033[32m 9. Intalling  dependencies of API Gatewary micro Service using pip \033[0m\n"
    sudo pip install -r SMS-Back-End/apigms/requirements.txt -t SMS-Back-End/apigms/lib/

    echo -e "\n\033[32m 10. Intalling  dependencies of Teaching Data Base micro Service using pip \033[0m\n"
    sudo pip install -r SMS-Back-End/tdbms/requirements.txt -t SMS-Back-End/tdbms/lib/

    echo -e "\n\033[32m 11. Intalling  dependencies of Students Control micro Service using pip \033[0m\n"
    sudo pip install -r SMS-Back-End/scms/requirements.txt -t SMS-Back-End/scms/lib/

    # Info message:
    echo "If any part of this automated proccess fail, please review requirementes_bash.sh to know more details about it."


else

    echo -e "\n\033[34m :( maybe in another moment \033[0m\n"

fi



