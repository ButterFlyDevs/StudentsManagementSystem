/**
  Fichero de creación de la base de datos de SMM--
  Uso:
    > mysql -u root -p < DBCreator.sql
  Ejecutado en el mismo directorio que este fichero.

  Versión 0.1

  Detalles:
  En la anterior versión 0 existía un identificador por curso que se componía
  con curso, grupo y nivel. El problema está en que para buscar por algúno de esos
  campos era imposible, por eso ahora se ha convertido en una clave primaria compuesta.
  Además se ha cambiado el nombre de la entidad "Curso" que hacía referencia a 1ºAESO por ejemplo
  por clase ya que existe el atributo "curso" (1º, 2º, 3º...) que chocaba con la definición de la entidad.

**/

#Borra la versión existente de la base de datos
DROP DATABASE IF EXISTS sms;

#Creamos la base de datos.
CREATE DATABASE sms;

#Entramos en su contexto
USE sms;

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

#Creación de la tabla Clase, ejemplo
CREATE TABLE Clase(
  curso INT(1),
  grupo CHAR(1),
  nivel CHAR(20),
  descripcion CHAR(200),
  #La clave primaria la forman los tres campos que juntos no pueden ser repetidos. (Sólo puede existir una entidad con ellos)
  PRIMARY KEY (curso, grupo, nivel)
);

#Creacion de la tabla para los Grupos
#Un grupo es la asociación de una asignatura y un curso, por ejemplo: 1ºESO-Francés que identifica perfectamente un grupo de alumnos.
CREATE TABLE Asocia(
 id_asignatura CHAR(10),
 curso INT(1),
 grupo CHAR(1),
 nivel CHAR(20),
 #Especificamos que se trata de claves foráneas (claves primarias de otras tablas)
 FOREIGN KEY (id_asignatura) REFERENCES Asignatura(id),
 FOREIGN KEY (curso, grupo, nivel) REFERENCES Clase(curso, grupo, nivel),


 #Especificamos la formación de la clave primaria en esta tabla.
 PRIMARY KEY (id_asignatura, curso, grupo, nivel)
);

CREATE TABLE Imparte(
  #Añadimos la referencia de la entidad Asignatura
  id_asignatura CHAR(10),
  curso INT(1),
  grupo CHAR(1),
  nivel CHAR(20),
  #Necesitamos una referncia del profesor:
  id_profesor CHAR(9),
  #Especificamos que se trata de claves foráneas.
  FOREIGN KEY (id_asignatura) REFERENCES Asignatura(id),
  FOREIGN KEY (curso, grupo, nivel) REFERENCES Clase(curso, grupo, nivel),
  FOREIGN KEY (id_profesor) REFERENCES Profesor(dni),
  #Establecemos la clave primaria compuesta.
  PRIMARY KEY (id_asignatura, curso, grupo, nivel, id_profesor)
);

CREATE TABLE Matricula(

  #Añadimos la referencia de la entidad Asignatura
  id_asignatura CHAR(10),
  curso INT(1),
  grupo CHAR(1),
  nivel CHAR(20),
  #Necesitamos una referncia del alumno:
  id_alumno CHAR(9),

  #Especificamos que se trata de claves foráneas.
  FOREIGN KEY (id_asignatura) REFERENCES Asignatura(id),
  FOREIGN KEY (curso, grupo, nivel) REFERENCES Clase(curso, grupo, nivel),
  FOREIGN KEY (id_alumno) REFERENCES Alumno(dni),
  #Establecemos la clave primaria compuesta.
  PRIMARY KEY (id_asignatura, curso, grupo, nivel, id_alumno)
);
