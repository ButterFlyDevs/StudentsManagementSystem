/**
  Fichero de creación de la base de datos de SMM--
  Uso:
    > mysql -u root -p < DBCreator.sql
  Ejecutado en el mismo directorio que este fichero.

  Versión 0.1
**/

#Borra la versión existente de la base de datos
DROP DATABASE IF EXISTS sms;

#Creamos la base de datos.
CREATE DATABASE sms;

#Entramos en su contexto
USE sms;

/*Creación de la tabla Alumno, con todos los atributos de esta entidad.
No usamos el DNI como clave primaria porque hasta los 14 años no es obligatorio
tener este documento, por eso usaremos un id entero autoincrementable.
Además usamos UNIQUE para establecer que no puedan existir elementos duplicados por ese valor
en la tabla. Así aunque no podrán existir dos alumnos que tengan exactamente el mismo nombre y apellidos
o el mismo DNI en caso de tenerlo.
*/
CREATE TABLE Alumno(
  id_alumno INT NOT NULL AUTO_INCREMENT,
  nombre CHAR(50),
  apellidos CHAR(100),
  dni INT,
  direccion CHAR(100),
  localidad CHAR(50),
  provincia CHAR(50),
  fecha_nacimiento DATE,
  telefono CHAR(50),
  PRIMARY KEY (id_alumno),

  #UNIQUE (nombre, apellidos), #puede que sea mejor quitarlo; González: Es mejor quitarlo. Es posible que dos alumnos se llamen igual.
  UNIQUE (dni)
);

/*Creación de la tabla Profesor, con todos los atributos de esta entidad.
En este caso si existe el dni para todos y puede usarse como pk, además no
permitiremos que existan dos personas con el mismo nombre y apellidos.
*/
CREATE TABLE Profesor(
  id_profesor INT NOT NULL AUTO_INCREMENT,
  nombre CHAR(50),
  apellidos CHAR(100),
  dni INT,
  direccion CHAR(100),
  localidad CHAR(50),
  provincia CHAR(50),
  fecha_nacimiento DATE,
  telefono CHAR(50),
  PRIMARY KEY (id_profesor),
  UNIQUE (nombre, apellidos)  #puede que sea mejor quitarlo.
);

#Creación de la tabla Asignatura, con todos los atributos de esta entidad.
CREATE TABLE Asignatura(
  id_asignatura INT NOT NULL AUTO_INCREMENT,
  nombre CHAR(100),
  PRIMARY KEY (id_asignatura),
  UNIQUE (nombre) #No se entiende que haya dos asignaturas con el mismo nombre exacto, por eso no se permite.
);

#Creación de la tabla Clase, ejemplo
CREATE TABLE Clase(
  id_clase INT NOT NULL AUTO_INCREMENT,
  curso INT(1),
  grupo CHAR(1),
  nivel CHAR(20),
  #La clave primaria la forman los tres campos que juntos no pueden ser repetidos. (Sólo puede existir una entidad con ellos)
  PRIMARY KEY (id_clase),
  #Hacemos que los tres campos sean UNIQUE para que no pueda exisir una clase con los mismos datos que otra
  UNIQUE (curso, grupo, nivel)
);

#Creacion de la tabla para los Grupos
#Un grupo es la asociación de una asignatura y un curso, por ejemplo: 1ºESO-Francés que identifica perfectamente un grupo de alumnos.
CREATE TABLE Asocia(

 id_asociacion INT NOT NULL AUTO_INCREMENT,
 id_clase INT ,
 id_asignatura INT,

 #Especificamos que se trata de claves foráneas (claves primarias de otras tablas)
 FOREIGN KEY (id_clase) REFERENCES Clase(id_clase),
 FOREIGN KEY (id_asignatura) REFERENCES Asignatura(id_asignatura),

 #Especificamos la formación de la clave primaria en esta tabla.
 PRIMARY KEY (id_asociacion),
 UNIQUE (id_clase, id_asignatura) #Para que no puedan repetirse
);

CREATE TABLE Imparte(

  id_imparte INT NOT NULL AUTO_INCREMENT,
  #Añadimos la referencia de la entidad Asignatura
  id_asociacion INT,
  #Necesitamos una referncia del profesor:
  id_profesor INT,

  #Especificamos que se trata de claves foráneas.
  FOREIGN KEY (id_asociacion) REFERENCES Asocia(id_asociacion),
#  FOREIGN KEY (id_asignatura) REFERENCES Asignatura(id_asignatura),
  FOREIGN KEY (id_profesor) REFERENCES Profesor(id_profesor),

  #Establecemos la clave primaria compuesta.
  PRIMARY KEY (id_imparte)

);

CREATE TABLE Matricula(

  id_matricula INT NOT NULL AUTO_INCREMENT,
  id_alumno INT,
  id_asociacion INT,



  #Especificamos que se trata de claves foráneas.
  FOREIGN KEY (id_asociacion) REFERENCES Asocia(id_asociacion),
  FOREIGN KEY (id_alumno) REFERENCES Alumno(id_alumno),

  #Establecemos la clave primaria compuesta.
  PRIMARY KEY (id_matricula)

);
