/**
  Fichero de creación de la base de datos de SMM--
  Uso:
    > mysql -u root -p < DBCreator.sql
  Ejecutado en el mismo directorio que este fichero.

**/

#Borra la versión existente de la base de datos
DROP DATABASE IF EXISTS smm;

#Creamos la base de datos.
CREATE DATABASE smm;

USE smm;

#Creación de la tabla Alumno
CREATE TABLE Alumno(
  nombre CHAR(20),
  dni CHAR(9),
  PRIMARY KEY (dni)
);


#Aprovisionamiento:
INSERT INTO Alumno VALUES('Nombre 1', 'xx');
INSERT INTO Alumno VALUES('Nombre 2', 'yy');
INSERT INTO Alumno VALUES('Nombre 3', 'zz');

#Prueba
SELECT * FROM Alumno;
