# -*- coding: utf-8 -*-

'''
Fichero que importa la librería para la conexión con MySQL con python. En este también se especifican las
variables de conexión con la BD en el entorno de desarrollo y se define la función conecta que
usan todas los subficheros de la API para conectarse con la base de datos.
'''

#Doc here: http://mysql-python.sourceforge.net/MySQLdb-1.2.2/
import MySQLdb

import os

#Variables de conexión de la BD en local
host='localhost'
user='root'
password='root'
db='sms'

#Variables de conexión a la instancia de Cloud SQL en producción, a partir de un fichero externo.
#El fichero tiene el siguiente contenido: _INTANCE_NAME='your-project-id:your-instance-name'
import productionCloudSQLInstanceINFO as psqlinfo


#Método de conexión, que se define de forma que sirva tanto en entorno DEV como en PRODUCCIÓN.
def conecta():

    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
        return MySQLdb.connect(unix_socket='/cloudsql/' + psqlinfo._INSTANCE_NAME, db=db, user='root', charset='utf8')
    else:
        return MySQLdb.connect(host, user, password, db, charset='utf8');


#Seteando el chartset a utf-8 en la conexión nos ahorramos de tener que establecer esto en cada conexión.


'''
Función extra para codificar el texto de la base de datos que está en utf8 de forma correcta para que pueda imprimirse
por terminal.
'''
def formatOutputText(cadena):
    return cadena.encode('utf-8')
