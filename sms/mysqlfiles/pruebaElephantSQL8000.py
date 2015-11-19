# -*- coding: utf-8 -*-
#Para instalar la librería:
#pip install pg8000

import pg8000

#Realizamos la conexión.
conexion = pg8000.connect(
    user='wirovhhd',
    host='hard-plum.db.elephantsql.com',
    unix_sock=None,
    port=   5432,
    database='wirovhhd',
    password='zOcBD509e4rzWuf7Gkj8lgQfK9BDGg-7',
    ssl=False,
    timout=None
)

cursor = conexion.cursor()
#cursor.execute(open("DBCreator_v01.sql", "r").read())
cursor.execute("INSERT INTO Asignatura VALUES ('Asig1', 'A1');")


'''
query="select * from Asignatura";

cursor.execute(query);

row = cursor.fetchone()

while row is not None:
    print row[0]
    print row[1]
    row = cursor.fetchone()

cursor.close()
conexion.close()
'''
