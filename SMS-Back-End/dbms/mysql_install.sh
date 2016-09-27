#!/usr/bin/env bash

# Script to install MySQL Server unattended with 'root' like user and password.

echo -e "\n\033[31m Installing  MySQL-Server unattended. \033[0m\n"

sudo apt-get update
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password root'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password root'
sudo apt-get --force-yes -y install mysql-server

echo -e "\033[31m"
echo "Done!"
mysql --version
echo "Run the daemon."
sudo /etc/init.d/mysql start
echo -e "If you have found some problem, try to install this manually."
echo -e "\033[0m"
