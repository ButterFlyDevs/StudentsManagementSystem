# -*- coding: utf-8 -*-

'''
Para conseguir los drivers de conexión con ElephantSQL usamos la librería psycopg2, como
especifica la página oficial: http://www.elephantsql.com/docs/python.html .

La instalación del driver se instala con:  sudo apt-get install python-psycopg2
Más datos sobre la librería: http://initd.org/psycopg/docs/install.html

Para trabajar con ORM en Sqlite Elephant recomienda usar SQLAlchemy

Para realizar la instalción en un directorio específico hacemos pip install -t smm/lib/ psycopg2
https://wiki.postgresql.org/wiki/Python

'''

import os
import psycopg2
import urlparse
import clavesElephantSQL

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(clavesElephantSQL.DATABASE_URL)
conn = psycopg2.connect(database=url.path[1:],
  user=url.username,
  password=url.password,
  host=url.hostname,
  port=url.port
)

cursor = conn.cursor()
cursor.execute(open("DBCreator_v01.sql", "r").read())



query="select * from Asignatura";

cursor.execute(query);

row = cursor.fetchone()

while row is not None:
    print row[0]
    print row[1]
    row = cursor.fetchone()

cursor.close()
