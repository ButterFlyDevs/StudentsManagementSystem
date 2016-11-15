/**
  Structure file creation of msDB Data Base.

  Example of use:
    > mysql -u root -p'root' < DBCreator.sql
**/


# First is removed the previous version of the database, if it exists.
DROP DATABASE IF EXISTS sms;

# Is created the database.
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
CREATE TABLE student (

  studentId       INT NOT NULL AUTO_INCREMENT,

  name            CHAR(50),
  surname         CHAR(100),
  dni             INT,
  email           CHAR(120),
  address         CHAR(100),
  locality        CHAR(50),
  province        CHAR(50),
  birthdate       DATE, #MySQL retrieves and displays DATE values in 'YYYY-MM-DD' format
  phone           CHAR(50),
  profileImageUrl CHAR(200),

  #Metadata parameters
  createdBy       INT,
  createdAt       DATETIME,
  modifiedBy      INT,
  modifiedAt      DATETIME,
  deletedBy       INT,
  deletedAt       DATETIME,
  deleted         BOOL,

  PRIMARY KEY (studentId)
  # UNIQUE (dni)
);

/*Creación de la tabla Profesor, con todos los atributos de esta entidad.
En este caso si existe el dni para todos y puede usarse como pk, además no
permitiremos que existan dos personas con el mismo nombre y apellidos.
*/

CREATE TABLE teacher (

  teacherId       INT NOT NULL AUTO_INCREMENT,

  name            CHAR(50),
  surname         CHAR(100),
  dni             INT,
  email           CHAR(120),
  address         CHAR(100),
  locality        CHAR(50),
  province        CHAR(50),
  birthdate       DATE, #MySQL retrieves and displays DATE values in 'YYYY-MM-DD' format
  phone           CHAR(50),
  profileImageUrl CHAR(200),

  #Metadata parameters
  createdBy       INT,
  createdAt       DATETIME,
  modifiedBy      INT,
  modifiedAt      DATETIME,
  deletedBy       INT,
  deletedAt       DATETIME,
  deleted         BOOL,

  PRIMARY KEY (teacherId)
  # UNIQUE (dni)
);

#Creación de la tabla Asignatura, con todos los atributos de esta entidad.
CREATE TABLE subject (

  subjectId   INT NOT NULL AUTO_INCREMENT,

  name        CHAR(100),
  description CHAR(255),

  #Metadata parameters
  createdBy   INT,
  createdAt   DATETIME,
  modifiedBy  INT,
  modifiedAt  DATETIME,
  deletedBy   INT,
  deletedAt   DATETIME,
  deleted     BOOL,

  PRIMARY KEY (subjectId)
  # UNIQUE (name) #No se entiende que haya dos asignaturas con el mismo nombre exacto, por eso no se permite.
);

#Creación de la tabla Clase, ejemplo
CREATE TABLE class (

  classId    INT NOT NULL AUTO_INCREMENT,

  course     INT(1),
  word       CHAR(1),
  level      CHAR(20),

  #Metadata parameters
  createdBy  INT,
  createdAt  DATETIME,
  modifiedBy INT,
  modifiedAt DATETIME,
  deletedBy  INT,
  deletedAt  DATETIME,
  deleted    BOOL,

  #La clave primaria la forman los tres campos que juntos no pueden ser repetidos. (Sólo puede existir una entidad con ellos)
  PRIMARY KEY (classId)
  #Hacemos que los tres campos sean UNIQUE para que no pueda exisir una clase con los mismos datos que otra
  # UNIQUE (course, word, level)
);

#Creacion de la tabla para los Grupos
#Un grupo es la asociación de una asignatura y un curso, por ejemplo: 1ºESO-Francés que identifica perfectamente un grupo de alumnos.
CREATE TABLE association (

  associationId INT NOT NULL AUTO_INCREMENT,

  classId       INT,
  subjectId     INT,

  #Metadata parameters
  createdBy     INT,
  createdAt     DATETIME,
  modifiedBy    INT,
  modifiedAt    DATETIME,
  deletedBy     INT,
  deletedAt     DATETIME,
  deleted       BOOL,

  #Especificamos que se trata de claves foráneas (claves primarias de otras tablas)
  FOREIGN KEY (subjectId) REFERENCES subject (subjectId),
  FOREIGN KEY (classId) REFERENCES class (classId),

  PRIMARY KEY (associationId)
  # UNIQUE (subjectId, classId)
);


CREATE TABLE impart (

  impartId      INT NOT NULL AUTO_INCREMENT,
  #Añadimos la referencia de la entidad Asignatura
  associationId INT,
  #Necesitamos una referncia del profesor:
  teacherId     INT,

  #Metadata parameters
  createdBy     INT,
  createdAt     DATETIME,
  modifiedBy    INT,
  modifiedAt    DATETIME,
  deletedBy     INT,
  deletedAt     DATETIME,
  deleted       BOOL,

  #Especificamos que se trata de claves foráneas.
  FOREIGN KEY (associationId) REFERENCES association (associationId),
  FOREIGN KEY (teacherId) REFERENCES teacher (teacherId),
  #Establecemos la clave primaria compuesta.
  PRIMARY KEY (impartId)
  # Especificamos que la formación idAsociacion, idProfesor) como par no pueda repetirse:
  # UNIQUE (associationId, teacherId)

);


CREATE TABLE enrollment (

  enrollmentId  INT NOT NULL AUTO_INCREMENT,

  studentId     INT,
  associationId INT,

  #Metadata parameters
  createdBy     INT,
  createdAt     DATETIME,
  modifiedBy    INT,
  modifiedAt    DATETIME,
  deletedBy     INT,
  deletedAt     DATETIME,
  deleted       BOOL,

  #Especificamos que se trata de claves foráneas.
  FOREIGN KEY (associationId) REFERENCES association (associationId),
  FOREIGN KEY (studentId) REFERENCES student (studentId),
  #Establecemos la clave primaria compuesta.
  PRIMARY KEY (enrollmentId)
  #Un alumno no puede estar dos veces matriuclado a la misma asociacion
  # UNIQUE (studentId, associationId)

);

/*
Se han eliminado los atributos unique para que puedan exsistir dos item que sean el mismo, debido a que uno fue creado
y luego eliminado mientras que otro fue creado después. Eso nos permite trazabilidad de los elementos repetidos
sin entrar en conflicto.
 */

/*
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
*/