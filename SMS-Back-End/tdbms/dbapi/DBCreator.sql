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

####################################
## STUDENT model table definition ##
####################################
CREATE TABLE student (

  studentId       INT NOT NULL AUTO_INCREMENT,

  name            CHAR(100) NOT NULL,
  surname         CHAR(100) NOT NULL,
  dni             INT,
  email           CHAR(120),
  address         CHAR(100),
  locality        CHAR(50),
  province        CHAR(50),
  birthdate       DATE, #MySQL retrieves and displays DATE values in 'YYYY-MM-DD' format
  phone           CHAR(50),
  profileImageUrl CHAR(200),
  gender          CHAR(1),

  #Metadata parameters
  createdBy       INT,
  createdAt       DATETIME,
  modifiedBy      INT,
  modifiedAt      DATETIME,
  deletedBy       INT,
  deletedAt       DATETIME,
  deleted         BOOL,

  PRIMARY KEY (studentId),
  UNIQUE (dni, deleted) # So, can't be exists two items with same dni if they is actives, but yeah if this is deleted,
  # because the deleted item will be to NULL and not conflict.
);

# Trigger to avoid NULL on items that have NOT NULL property, is necessary with our design.
DELIMITER $$
CREATE TRIGGER avoid_empty_on_student_trigger
    BEFORE INSERT ON student
        FOR EACH ROW
        BEGIN
        IF NEW.name = '' THEN SET NEW.name = NULL;
        END IF;
        END $$
DELIMITER ;




/*Creación de la tabla Profesor, con todos los atributos de esta entidad.
En este caso si existe el dni para todos y puede usarse como pk, además no
permitiremos que existan dos personas con el mismo nombre y apellidos.
*/

####################################
## TEACHER model table definition ##
####################################
CREATE TABLE teacher (

  teacherId       INT NOT NULL AUTO_INCREMENT,

  name            CHAR(100) NOT NULL,
  surname         CHAR(100) NOT NULL,
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

  PRIMARY KEY (teacherId),
  UNIQUE (dni, deleted)
);

# Trigger to avoid NULL on items that have NOT NULL property, is necessary with our design.
DELIMITER $$
CREATE TRIGGER avoid_empty_on_teacher_trigger
    BEFORE INSERT ON teacher
        FOR EACH ROW
        BEGIN
        IF NEW.name = '' THEN SET NEW.name = NULL;
        END IF;
        END $$
DELIMITER ;

####################################
## SUBJECT model table definition ##
####################################
CREATE TABLE subject (

  subjectId   INT NOT NULL AUTO_INCREMENT,

  name        CHAR(100) NOT NULL,
  description CHAR(255),

  #Metadata parameters
  createdBy   INT,
  createdAt   DATETIME,
  modifiedBy  INT,
  modifiedAt  DATETIME,
  deletedBy   INT,
  deletedAt   DATETIME,
  deleted     BOOL,

  PRIMARY KEY (subjectId),
  UNIQUE (name, deleted)
);

# Trigger to avoid NULL on items that have NOT NULL property, is necessary with our design.
DELIMITER $$
CREATE TRIGGER avoid_empty_on_subject_trigger
    BEFORE INSERT ON subject
        FOR EACH ROW
        BEGIN
        IF NEW.name = '' THEN SET NEW.name = NULL; END IF;
        END $$
DELIMITER ;

#Creación de la tabla Clase, ejemplo
####################################
## CLASS model table definition   ##
####################################
CREATE TABLE class (

  #Item identifier
  classId    INT NOT NULL AUTO_INCREMENT,

  course     INT(1) NOT NULL,
  word       CHAR(10) NOT NULL,
  level      CHAR(20) NOT NULL,

  description CHAR(255),

  #Metadata attributes
  createdBy  INT,
  createdAt  DATETIME,
  modifiedBy INT,
  modifiedAt DATETIME,
  deletedBy  INT,
  deletedAt  DATETIME,
  deleted    BOOL,

  PRIMARY KEY (classId),
  UNIQUE (course, word, level, deleted)
);





# Control when a item of class is "logically deleted".
DELIMITER $$
CREATE TRIGGER tr_class
BEFORE INSERT ON class FOR EACH ROW
  BEGIN

    IF NEW.course = '' THEN SET NEW.course = NULL; END IF;
    IF NEW.word = '' THEN SET NEW.word = NULL; END IF;
    IF NEW.level = '' THEN SET NEW.level = NULL; END IF;

    # Si se trata de un grupo de optatividad tenemos que comprobar que cumple las condiciones de insercción:

    IF NEW.word NOT REGEXP '^[A-Z]{1}$' THEN # Si no cumple la expresión regular se trata de un grupo de optatividad:
      #Entonces procedemos a dividir el string para obtener los valores gr (grupo) y subgr (subgrupo)
      #SIGNAL SQLSTATE '45000'
      #SET MESSAGE_TEXT = 'Se trata de una OPTATIVA ';

      #Una vez obtenidos comprobaemos si puede o no realizarse la insercción bajo nuestra lógica, que es más
      #sencilla de implementar aquí y es más segura que haciéndola programaticamente fuera del motor.

      set @grp =  SUBSTRING(NEW.word, 5, 1); # The number of group.
      set @subgrp = SUBSTRING(NEW.word, 7, 1); # The number of subgroup.

      #Checking that the numbers are numbers and nothing more.
      IF @grp NOT REGEXP '^[1-9]{1}$' THEN
          SIGNAL SQLSTATE '45000'
          SET MESSAGE_TEXT = 'Formato no aceptable';
      END IF;

      IF @grp NOT REGEXP '^[1-9]{1}$' THEN
          SIGNAL SQLSTATE '45000'
          SET MESSAGE_TEXT = 'Formato no aceptable';
      END IF;


      IF @subgrp > 1 THEN

        set @subgrp = @subgrp - 1;
        set @tosearch = concat('OPT_', @grp, '_', @subgrp);
        IF NOT EXISTS (SELECT word FROM class where word = @tosearch and deleted = '0') THEN   # Only active items.
          SIGNAL SQLSTATE '45000'
          SET MESSAGE_TEXT = 'Impossible insert, should be exists a subgroup lower, and this broke the consistency.';
        END IF;

      ELSEIF @grp > 1 THEN

        set @grp = @grp - 1;
        set @tosearch = concat('OPT_', @grp, '_', @subgrp);
        IF NOT EXISTS (SELECT word FROM class where word = @tosearch and deleted = '0') THEN   # Only active items.
          SIGNAL SQLSTATE '45000'
          SET MESSAGE_TEXT = 'Impossible insert, should be exists a group lower, and this broke the consistency.';
        END IF;

      END IF;

    END IF;
  END$$
DELIMITER ;



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

  PRIMARY KEY (associationId),
  UNIQUE (subjectId, classId, deleted)
);

DELIMITER $$
CREATE TRIGGER avoid_fail_references_on_association_insertions_trigger
    BEFORE INSERT ON association
        FOR EACH ROW
        BEGIN
         IF NOT EXISTS (SELECT * FROM subject where subjectId = NEW.subjectId and deleted = '0') THEN   # Only active items.
          SIGNAL SQLSTATE '45000'
          SET MESSAGE_TEXT = 'Impossible insert the association, the subject related should be exists , and this broke the consistency.';
         END IF;
         IF NOT EXISTS (SELECT * FROM class where classId = NEW.classId and deleted = '0') THEN   # Only active items.
          SIGNAL SQLSTATE '45000'
          SET MESSAGE_TEXT = 'Impossible insert the association, the class related should be exists , and this broke the consistency.';
         END IF;
        END $$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER update_subject_trigger
BEFORE UPDATE ON subject FOR EACH ROW
  BEGIN

     IF EXISTS (SELECT * FROM association where subjectId = NEW.subjectId and deleted IS NOT NULL and NEW.deleted IS NULL) THEN   # Only active items.
          SIGNAL SQLSTATE '45000'
          SET MESSAGE_TEXT = 'Impossible delete the subject, this is related with some class , and this broke the consistency.';
     END IF;
  END$$
DELIMITER ;

# Control when a item of class is "logically deleted".
DELIMITER $$
CREATE TRIGGER update_class_trigger
BEFORE UPDATE ON class FOR EACH ROW
  BEGIN

     IF EXISTS (SELECT * FROM association where classId = NEW.classId and deleted IS NOT NULL and NEW.deleted IS NULL) THEN   # Only active items.
          SIGNAL SQLSTATE '45000'
          SET MESSAGE_TEXT = 'Impossible delete the class, this is related with some subject , and this broke the consistency.';
     END IF;

    #Si viene a eliminar el item tenemos que comprobar ciertas cosas:
    IF NEW.deleted IS NULL THEN

      #Si ya está eliminado no lo podemos eliminar otra vez.
      IF EXISTS (SELECT * FROM class where classId = NEW.classId AND deleted IS NULL) THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = '404 Not found';
      END IF;

      #Se trata de un grupo de optatividad?
      #Para ello tenemos que extraer el word:
      SET @wordSearched = (SELECT word FROM class where classId = NEW.classId);
      IF @wordSearched NOT REGEXP '^[A-Z]{1}$' THEN # Se trata de una optativa y hay que comprobar las condiciones.

        set @grp =  SUBSTRING(@wordSearched, 5, 1); # The number of group.
        set @subgrp = SUBSTRING(@wordSearched, 7, 1); # The number of subgroup

        set @subgrp = @subgrp + 1;
          set @tosearch = concat('OPT_', @grp, '_', @subgrp);
          IF EXISTS (SELECT word FROM class where word = @tosearch AND deleted IS NOT NULL) THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Imposible deleting, there are a subgroup higher, and this broke the consistency.';
          END IF;

        set @grp = @grp + 1;
          set @tosearch = concat('OPT_', @grp, '_', @subgrp);
          IF EXISTS (SELECT word FROM class where word = @tosearch AND deleted IS NOT NULL) THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Imposible deleting, there are a group higher, and this broke the consistency.';
          END IF;
      END IF;
    END IF;

  END$$
DELIMITER ;

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
  PRIMARY KEY (impartId),
  # Especificamos que la formación idAsociacion, idProfesor) como par no pueda repetirse:
  UNIQUE (associationId, teacherId, deleted)

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
  PRIMARY KEY (enrollmentId),
  #Un alumno no puede estar dos veces matriuclado a la misma asociacion
  UNIQUE (studentId, associationId, deleted)

);

#################################
## enrollment table triggers   ##
#################################

DELIMITER $$
CREATE TRIGGER avoid_fail_references_on_enrollment_insertions_trigger
    BEFORE INSERT ON enrollment
        FOR EACH ROW
        BEGIN
         IF NOT EXISTS (SELECT * FROM association where associationId = NEW.associationId and deleted IS NOT NULL) THEN   # Only active items.
          SIGNAL SQLSTATE '45000'
          SET MESSAGE_TEXT = 'Impossible insert the enrollment, the association related should be exists , and this broke the consistency.';
         END IF;
         IF NOT EXISTS (SELECT * FROM student where studentId = NEW.studentId and deleted IS NOT NULL) THEN   # Only active items.
          SIGNAL SQLSTATE '45000'
          SET MESSAGE_TEXT = 'Impossible insert the enrollment, the student related should be exists , and this broke the consistency.';
         END IF;
        END $$
DELIMITER ;

#################################
##    impart table triggers    ##
#################################

DELIMITER $$
CREATE TRIGGER avoid_fail_references_on_impart_insertions_trigger
    BEFORE INSERT ON impart
        FOR EACH ROW
        BEGIN
         IF NOT EXISTS (SELECT * FROM association where associationId = NEW.associationId and deleted IS NOT NULL) THEN   # Only active items.
          SIGNAL SQLSTATE '45000'
          SET MESSAGE_TEXT = 'Impossible insert the impart, the association related should be exists , and this broke the consistency.';
         END IF;
         IF NOT EXISTS (SELECT * FROM teacher where teacherId = NEW.teacherId and deleted IS NOT NULL) THEN   # Only active items.
          SIGNAL SQLSTATE '45000'
          SET MESSAGE_TEXT = 'Impossible insert the impart, the teacher related should be exists , and this broke the consistency.';
         END IF;
        END $$
DELIMITER ;





##############################
## student table triggers   ##
##############################

DELIMITER $$
CREATE TRIGGER avoid_fail_references_with_enrollment_student_trigger
    BEFORE UPDATE ON student
    FOR EACH ROW
    BEGIN

      # Checking references in ENROLLMENT table.
     IF EXISTS (SELECT * FROM enrollment where studentId = NEW.studentId and deleted IS NOT NULL and NEW.deleted IS NULL) THEN   # Only check active items.
              SIGNAL SQLSTATE '45000'
              SET MESSAGE_TEXT = 'Impossible delete the student, this is related with some association in enrollment table, and this broke the consistency.';
     END IF;

    END $$
DELIMITER ;

##############################
## teacher table triggers   ##
##############################

DELIMITER $$
CREATE TRIGGER avoid_fail_references_with_impart_teacher_trigger
    BEFORE UPDATE ON teacher
    FOR EACH ROW
    BEGIN
     IF EXISTS (SELECT * FROM impart where teacherId = NEW.teacherId and deleted IS NOT NULL and NEW.deleted IS NULL) THEN   # Only active items.
              SIGNAL SQLSTATE '45000'
              SET MESSAGE_TEXT = 'Impossible delete the teacher, this is related with some association in impart table, and this broke the consistency.';
             END IF;
    END $$
DELIMITER ;

#################################
## associaton table triggers   ##
#################################

DELIMITER $$
CREATE TRIGGER avoid_fail_references_with_enrollment_association_trigger
    BEFORE UPDATE ON association
    FOR EACH ROW
    BEGIN
     IF EXISTS (SELECT * FROM enrollment where associationId = NEW.associationId and deleted IS NOT NULL) THEN   # Only active items.
              SIGNAL SQLSTATE '45000'
              SET MESSAGE_TEXT = 'Impossible delete the association, this is related with some student in enrollment table, and this broke the consistency.';
     END IF;
      IF EXISTS (SELECT * FROM impart where associationId = NEW.associationId and deleted IS NOT NULL) THEN   # Only active items.
              SIGNAL SQLSTATE '45000'
              SET MESSAGE_TEXT = 'Impossible delete the association, this is related with some teacher in impart table, and this broke the consistency.';
     END IF;
    END $$
DELIMITER ;



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



