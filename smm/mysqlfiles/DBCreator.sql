/**
  Fichero de creación de la base de datos de SMM--
  Uso:
    > mysql -u root -p < DBCreator.sql
  Ejecutado en el mismo directorio que este fichero.

**/

DROP DATABASE smm;

#Creamos la base de datos.
CREATE DATABASE smm;

USE smm;

#Creación de la tabla Alumno
CREATE TABLE Alumno(
  nombre CHAR(20),
  dni CHAR(9),
  PRIMARY KEY (dni)
);

#Creación de la tabla Asignatura
CREATE TABLE Asignatura(
  nombre CHAR(20),
  id CHAR(9),
  PRIMARY KEY (id)
);

#Creación de la tabla Profesor
CREATE TABLE Profesor(
  nombre CHAR(20),
  dni CHAR(9),
  PRIMARY KEY(dni)
);

CREATE TABLE Imparte(
  dniProfesor CHAR(9),
  idAsignatura CHAR(20),
  FOREIGN KEY (dniProfesor) REFERENCES Profesor(dni),
  FOREIGN KEY (idAsignatura) REFERENCES Asignatura(id)
);

CREATE TABLE Cursa(
  dniAlumno CHAR(9),
  idAsignatura CHAR(9),
  FOREIGN KEY (dniAlumno) REFERENCES Alumno(dni),
  FOREIGN KEY (idAsignatura) REFERENCES Asignatura(id)
);

/**
Inserción de datos de prueba.
**/
INSERT INTO Alumno VALUES('Nombre 1', 'xx');
INSERT INTO Alumno VALUES('Nombre 2', 'yy');
INSERT INTO Alumno VALUES('Nombre 3', 'zz');

INSERT INTO Asignatura VALUES ('Asig1', 'A1');
INSERT INTO Asignatura VALUES ('Asig2', 'A2');
INSERT INTO Asignatura VALUES ('Asig3', 'A3');

INSERT INTO Profesor VALUES('Prof 1', 'yy');
INSERT INTO Profesor VALUES('Prof 2', 'vv');
INSERT INTO Profesor VALUES('Prof 3', 'ww');

#El alumno con DNI xx cursa la asignatura de código A1.
INSERT INTO Cursa VALUES('xx','A1');
#El alumno con DNI yy cursa la asignatura de código A1.
INSERT INTO Cursa VALUES('yy','A1');
INSERT INTO Cursa VALUES('zz','A2');

#El profesor con DNI yy imparte la asignatura A1.
INSERT INTO Imparte VALUES('yy','A1');
#El profesor con DNI ww imparte la asignatura A2.
INSERT INTO Imparte VALUES('ww','A2');


/*
Si ahora quisiéramos saber a que alumnos imparte clase el profesor de nombre , ¿Cómo sería la consulta?
mysql> select Alumno.nombre  from Profesor, Imparte, Cursa, Alumno where Profesor.dni=Imparte.dniProfesor and Imparte.idAsignatura=Cursa.idAsignatura and Cursa.dniAlumno=Alumno.dni and Profesor.nombre="Prof 1";
+----------+
| nombre   |
+----------+
| Nombre 1 |
| Nombre 2 |
+----------+
2 rows in set (0,00 sec)

Para nombre="Prof 2"
Empty set (0,00 sec)

Para nombre="Profe 3"
+----------+
| nombre   |
+----------+
| Nombre 3 |
+----------+
1 row in set (0,00 sec)



*/


/**
Si intentásemos hacer: INSERT INTO Cursa VALUES('xx','A5');
nos daría un fallo referente a la clave foránea, no puede añadir que un alumno (xx) vaya
a cursar una asignatura A5 que no existe en el sistema.
**/
