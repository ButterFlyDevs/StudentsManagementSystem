/**
  Fichero de creación de la base de datos de SMM
  Uso:
    > mysql -u root -p'root' < DBCreator1.sql
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
tener este documento, por eso usaremos un id entero AUTO_INCREMENTable.
Además usamos UNIQUE para establecer que no puedan existir elementos duplicados por ese valor
en la tabla. Así aunque no podrán existir dos alumnos que tengan exactamente el mismo nombre y apellidos
o el mismo DNI en caso de tenerlo.
*/
CREATE TABLE Alumno(
  idAlumno INT NOT NULL AUTO_INCREMENT,
  nombre CHAR(50),
  apellidos CHAR(100),
  dni INT,
  direccion CHAR(100),
  localidad CHAR(50),
  provincia CHAR(50),
  #MySQL retrieves and displays DATE values in 'YYYY-MM-DD' format
  fechaNacimiento DATE,
  telefono CHAR(50),
  urlImagen CHAR (200),

  PRIMARY KEY (idAlumno),

  #UNIQUE (nombre, apellidos), #puede que sea mejor quitarlo; González: Es mejor quitarlo. Es posible que dos alumnos se llamen igual.
  UNIQUE (dni)
);


/*Creación de la tabla Profesor, con todos los atributos de esta entidad.
En este caso si existe el dni para todos y puede usarse como pk, además no
permitiremos que existan dos personas con el mismo nombre y apellidos.
*/
CREATE TABLE Profesor(
  idProfesor INT NOT NULL AUTO_INCREMENT,
  nombre CHAR(50),
  apellidos CHAR(100),
  dni INT,
  direccion CHAR(100),
  localidad CHAR(50),
  provincia CHAR(50),
  #MySQL retrieves and displays DATE values in 'YYYY-MM-DD' format
  fechaNacimiento DATE,
  telefono CHAR(50),
  PRIMARY KEY (idProfesor),
  UNIQUE (dni)
);

#Creación de la tabla Asignatura, con todos los atributos de esta entidad.
CREATE TABLE Asignatura(
  idAsignatura INT NOT NULL AUTO_INCREMENT,
  nombre CHAR(100),
  PRIMARY KEY (idAsignatura),
  UNIQUE (nombre) #No se entiende que haya dos asignaturas con el mismo nombre exacto, por eso no se permite.
);

#Creación de la tabla Clase, ejemplo
CREATE TABLE Clase(
  idClase INT NOT NULL AUTO_INCREMENT,
  curso INT(1),
  grupo CHAR(1),
  nivel CHAR(20),
  #La clave primaria la forman los tres campos que juntos no pueden ser repetidos. (Sólo puede existir una entidad con ellos)
  PRIMARY KEY (idClase),
  #Hacemos que los tres campos sean UNIQUE para que no pueda exisir una clase con los mismos datos que otra
  UNIQUE (curso, grupo, nivel)
);

#Creacion de la tabla para los Grupos
#Un grupo es la asociación de una asignatura y un curso, por ejemplo: 1ºESO-Francés que identifica perfectamente un grupo de alumnos.
CREATE TABLE Asociacion(
 idAsociacion INT NOT NULL AUTO_INCREMENT,
 idClase INT,
 idAsignatura INT,
 #Especificamos que se trata de claves foráneas (claves primarias de otras tablas)
 FOREIGN KEY (idClase) REFERENCES Clase(idClase),
 FOREIGN KEY (idAsignatura) REFERENCES Asignatura(idAsignatura),
 #Especificamos la formación de la clave primaria en esta tabla.
 PRIMARY KEY (idAsociacion),
 UNIQUE (idClase, idAsignatura) #Para que no puedan repetirse
);

CREATE TABLE Imparte(

  idImparte INT NOT NULL AUTO_INCREMENT,
  #Añadimos la referencia de la entidad Asignatura
  idAsociacion INT,
  #Necesitamos una referncia del profesor:
  idProfesor INT,
  #Especificamos que se trata de claves foráneas.
  FOREIGN KEY (idAsociacion) REFERENCES Asociacion(idAsociacion),
  FOREIGN KEY (idProfesor) REFERENCES Profesor(idProfesor),
  #Establecemos la clave primaria compuesta.
  PRIMARY KEY (idImparte),
  #Especificamos que la formación idAsociacion, idProfesor) como par no pueda repetirse:
  UNIQUE (idAsociacion, idProfesor)

);

CREATE TABLE Matricula(

  idMatricula INT NOT NULL AUTO_INCREMENT,
  idAlumno INT,
  idAsociacion INT,
  #Especificamos que se trata de claves foráneas.
  FOREIGN KEY (idAsociacion) REFERENCES Asociacion(idAsociacion),
  FOREIGN KEY (idAlumno) REFERENCES Alumno(idAlumno),
  #Establecemos la clave primaria compuesta.
  PRIMARY KEY (idMatricula),
  #Un alumno no puede estar dos veces matriuclado a la misma asociacion
  UNIQUE (idAlumno, idAsociacion)

);

CREATE TABLE Credenciales(

  idCredenciales INT NOT NULL AUTO_INCREMENT,
  idUsuario INT,
  nombre CHAR(100),
  username CHAR(100),
  password VARBINARY(150) NOT NULL,
  rol CHAR(50),
  PRIMARY KEY (idCredenciales),
  #Para que no pueda haber dos usuario con el mismo nombre
  UNIQUE (username)
);
