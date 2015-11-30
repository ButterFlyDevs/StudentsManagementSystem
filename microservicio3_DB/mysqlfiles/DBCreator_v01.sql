/**
  Fichero de creación de la base de datos de SMM--
  Adaptación para postgresql.
  Ojo: Los comentarios en en los ficheros .sql para postgresql no acepta almohadilla para comentarios.
**/


/**En postgresql no es necesario seleccionar base de datos porque ya está seleccionada y en uso al conectarse ya que en una
misma conexión no puede pasarte de una base de datos a otra en la misma conexión.
**/

CREATE TABLE Alumno(
  dni CHAR(9),
  nombre CHAR(20),
  PRIMARY KEY (dni)
);


CREATE TABLE Asignatura(
  id CHAR(9),
  nombre CHAR(20),
  PRIMARY KEY (id)
);


CREATE TABLE Profesor(
  dni CHAR(9),
  nombre CHAR(50),
  apellidos CHAR(50),
  municipio CHAR(50),
  provincia CHAR(50),
  domicilio CHAR(100),
  email CHAR(100),
  telefono CHAR(10),
  PRIMARY KEY(dni)
);

CREATE TABLE Grupo(
  curso CHAR(2),
  letra char(1),
  PRIMARY KEY(curso,letra)
);

CREATE TABLE Pertenece(
  curso_p CHAR(2),
  letra_p char(1),
  idAsignatura_p CHAR(9),
  PRIMARY KEY (curso_p,letra_p,idAsignatura_p),
  FOREIGN KEY (curso_p, letra_p) REFERENCES Grupo (curso, letra),
  FOREIGN KEY (idAsignatura_p) REFERENCES Asignatura (id)
);

CREATE TABLE Imparte(
  curso_i CHAR(2),
  letra_i char(1),
  idAsignatura_i CHAR(20),
  dniProfesor CHAR(9),
  PRIMARY KEY(curso_i,letra_i,idAsignatura_i,dniProfesor),
  FOREIGN KEY (dniProfesor) REFERENCES Profesor(dni),
  FOREIGN KEY (curso_i,letra_i,idAsignatura_i) REFERENCES Pertenece (curso_p, letra_p, idAsignatura_p)
);

CREATE TABLE Cursa(
  curso_c CHAR(2),
  letra_c char(1),
  idAsignatura_c CHAR(20),
  dniAlumno CHAR(9),
  PRIMARY KEY(curso_c,letra_c,idAsignatura_c,dniAlumno),
  FOREIGN KEY (dniAlumno) REFERENCES Alumno (dni),
  FOREIGN KEY (curso_c, letra_c, idAsignatura_c) REFERENCES Pertenece (curso_p, letra_p, idAsignatura_p)
);

INSERT INTO Asignatura VALUES ('Asig1', 'A1');
INSERT INTO Asignatura VALUES ('Asig2', 'A2');
INSERT INTO Asignatura VALUES ('Asig3', 'A3');

/**
Inserción de datos de prueba.
**/
/**
INSERT INTO Profesor VALUES('Emilio','Robot', 'xxxxxxxxZ','Albolote','Granada','C/La colmena','emilio@correo.com','600112233');
INSERT INTO Profesor VALUES('Lucia','Robertson', 'xxxxxxxxY','Pulianas','Granada','C/La mancha azul','Lucia@correo.com','500212121');

INSERT INTO Alumno VALUES('Nombre 1', 'xx');
INSERT INTO Alumno VALUES('Nombre 2', 'yy');
INSERT INTO Alumno VALUES('Nombre 3', 'zz');

INSERT INTO Asignatura VALUES ('Asig1', 'A1');
INSERT INTO Asignatura VALUES ('Asig2', 'A2');
INSERT INTO Asignatura VALUES ('Asig3', 'A3');

#El alumno con DNI xx cursa la asignatura de código A1.
INSERT INTO Cursa VALUES('xx','A1');
#El alumno con DNI yy cursa la asignatura de código A1.
INSERT INTO Cursa VALUES('yy','A1');
INSERT INTO Cursa VALUES('zz','A2');

#El profesor con DNI yy imparte la asignatura A1.
INSERT INTO Imparte VALUES('xxxxxxxxZ','A1');
#El profesor con DNI ww imparte la asignatura A2.
INSERT INTO Imparte VALUES('xxxxxxxxY','A2');
**/
