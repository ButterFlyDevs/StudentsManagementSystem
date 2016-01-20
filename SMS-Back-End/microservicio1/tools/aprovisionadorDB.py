# -*- coding: utf-8 -*-

#Fichero que cargará de contenido la base de datos para pruebas o cualquier otro menester.

import MySQLdb

db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="smm");
cursor = db.cursor()

MAX=5

#Aprovisionamos de contenido la tabla Alumnos
'''
Esquema de la tabla:
CREATE TABLE Alumno(
  nombre CHAR(20),
  dni CHAR(9),
  direccion CHAR(100),
  localidad CHAR(50),
  provincia CHAR(50),
  fecha_nacimiento DATE,
  telefono CHAR(50),
  PRIMARY KEY (dni)
);
'''
for i in range(0,MAX):
    nombre='\'Alumno'+str(i)+'\''
    dni=str(i)
    direccion='\'Direccion'+str(i)+'\''
    localidad='\'Localidad'+str(i)+'\''
    provincia='\'Provincia'+str(i)+'\''
    fecha_nac='\'1988-10-'+str(i+1)+'\''
    telefono='\''+str(i)+str(i)+str(i)+str(i)+'\''
    query="INSERT INTO Alumno VALUES("+nombre+","+dni+","+direccion+","+localidad+","+provincia+","+fecha_nac+","+telefono+");"
    print query
    salida = cursor.execute(query);
    #Ejecutamos la acción
    db.commit()

###### Aprovisionamos de contenido la tabla Profesor
'''
Esquema de la tabla:
CREATE TABLE Profesor(
  nombre CHAR(20),
  dni CHAR(9),
  direccion CHAR(100),
  localidad CHAR(50),
  provincia CHAR(50),
  fecha_nacimiento CHAR(50),
  telefonoA CHAR(50),
  telefonoB CHAR(50),
  PRIMARY KEY (dni)
);
'''
for i in range(0, MAX):
    nombre='\'Profesor'+str(i)+'\''
    dni=str(i)
    direccion='\'Direccion'+str(i)+'\''
    localidad='\'Localidad'+str(i)+'\''
    provincia='\'Provincia'+str(i)+'\''
    fecha_nac='\'1988-10-'+str(i+1)+'\''
    telefonoA='\''+str(i)+str(i)+str(i)+str(i)+'\''
    telefonoB='\''+str(i)+str(i)+str(i)+str(i)+'\''
    query="INSERT INTO Profesor VALUES("+nombre+","+dni+","+direccion+","+localidad+","+provincia+","+fecha_nac+","+telefonoA+","+telefonoB+");"
    print query
    salida = cursor.execute(query);
    #Ejecutamos la acción
    db.commit()

######Aprovisionamos de contenido la tabla Asignatura
'''
Esquema de la tabla:
CREATE TABLE Asignatura(
  id CHAR(10),
  nombre CHAR(20),
  PRIMARY KEY (id)
);
'''
for i in range(0, MAX):
    id='\''+str(i)+'\''
    nombre='\'Asignatura'+str(i)+'\''
    query="INSERT INTO Asignatura VALUES("+id+","+nombre+");"
    print query
    salida = cursor.execute(query);
    #Ejecutamos la acción
    db.commit()

######Aprovisionamos de contenido la tabla Curso
'''
Esquema de la tabla:
CREATE TABLE Curso(
  curso INT(1),
  grupo CHAR(1),
  nivel CHAR(20),
  PRIMARY KEY (curso)
);
'''
for i in range(0, MAX):
    curso='\''+str(i+1)+'\'' #curso 1º :1
    grupo='\''+str(i)+'\''   #grupo B  :B
    nivel='\'Nivel'+str(i)+'\'' #nivel ESO: ESO
    query="INSERT INTO Curso VALUES("+curso+","+grupo+","+nivel+");"
    print query
    salida = cursor.execute(query);
    #Ejecutamos la acción
    db.commit()







#Cerramos la conexión
cursor.close()
db.close()
