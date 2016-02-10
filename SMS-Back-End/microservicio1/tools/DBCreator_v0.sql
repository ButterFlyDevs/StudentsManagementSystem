/**
  Fichero de creación de la base de datos de SMM--
  Uso:
    > mysql -u root -p < DBCreator.sql
  Ejecutado en el mismo directorio que este fichero.

  ## Atención: Cualquier modificación de este fichero implica tener que modificar    ##
  ## el fichero aprovisionadorDB.py que llena de contenido la BD para que no falle.  ##

  #Notas:
    1º. Habría que evaluar el uso de eliminación en cascada en los casos en los que sean necesarios.
    2º. Habrá que justificar el uso del motor innoDB en las tablas

**/

#Borra la versión existente de la base de datos
DROP DATABASE IF EXISTS smm;

#Creamos la base de datos.
CREATE DATABASE smm;

USE smm;

#Creación de la tabla Alumno, con todos los atributos de esta entidad.
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

#Creación de la tabla Profesor, con todos los atributos de esta entidad.
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

#Creación de la tabla Asignatura, con todos los atributos de esta entidad.
CREATE TABLE Asignatura(
  id CHAR(10),
  nombre CHAR(20),
  PRIMARY KEY (id)
);

#Creación de la tabla Curso, ejemplo
CREATE TABLE Curso(
  #El id será la concatenación de los tres siguientes campos. Por ejemplo: 1AESO, 2CBACH (aunque en principio no se use)
  id CHAR(22),
  curso INT(1),
  grupo CHAR(1),
  nivel CHAR(20),
  PRIMARY KEY (id)
);

#Creacion de la tabla para los Grupos
#Un grupo es la asociación de una asignatura y un curso, por ejemplo: 1ºESO-Francés que identifica perfectamente un grupo de alumnos.
CREATE TABLE Asocia(
 id_asignatura CHAR(10),
 id_curso CHAR(22),
 #Especificamos que se trata de claves foráneas (claves primarias de otras tablas)
 FOREIGN KEY (id_asignatura) REFERENCES Asignatura(id),
 FOREIGN KEY (id_curso) REFERENCES Curso(id),
 #Especificamos la formación de la clave primaria en esta tabla.
 PRIMARY KEY (id_asignatura, id_curso)
);

#Si intentamos añadir una Asociación en Asocia y no tenemos los objetos previamente creandosno dará un error por incumplir las reglas de integridad referencial establecidas en la creación de la tablaCannot add or update a child row: a foreign key constraint fails, además del mensaje de error.Si tenemos creadas ambos datos no da problema.



CREATE TABLE Imparte(
  #Añadimos la referencia de la entidad Asignatura
  id_asignatura CHAR(10),
  #Añadimos la referencia de la entidad Curso
  id_curso CHAR(22),
  #Necesitamos una referncia del profesor:
  id_profesor CHAR(9),
  #Especificamos que se trata de claves foráneas.
  FOREIGN KEY (id_asignatura) REFERENCES Asignatura(id),
  FOREIGN KEY (id_curso) REFERENCES Curso(id),
  FOREIGN KEY (id_profesor) REFERENCES Profesor(dni),
  #Establecemos la clave primaria compuesta.
  PRIMARY KEY (id_asignatura, id_curso, id_profesor)
);

CREATE TABLE Matricula(

  #Añadimos la referencia de la entidad Asignatura
  id_asignatura CHAR(10),
  #Añadimos la referencia de la entidad Curso
  id_curso CHAR(22),
  #Necesitamos una referncia del alumno:
  id_alumno CHAR(9),

  #Especificamos que se trata de claves foráneas.
  FOREIGN KEY (id_asignatura) REFERENCES Asignatura(id),
  FOREIGN KEY (id_curso) REFERENCES Curso(id),
  FOREIGN KEY (id_alumno) REFERENCES Alumno(dni),
  #Establecemos la clave primaria compuesta.
  PRIMARY KEY (id_asignatura, id_curso, id_alumno)
);
