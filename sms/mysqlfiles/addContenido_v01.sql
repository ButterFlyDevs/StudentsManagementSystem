#         ### Insercción de datos de prueba. ###

#Inserción de profesores:
INSERT INTO Profesor VALUES('Emilio','Robot', 'xxxxxxxxZ','Albolote','Granada','C/La colmena','emilio@correo.com','600112233');
INSERT INTO Profesor VALUES('Lucia','Robertson', 'xxxxxxxxY','Pulianas','Granada','C/La mancha azul','Lucia@correo.com','500212121');

#Inserción de alumnos:
INSERT INTO Alumno VALUES('Andrés', 'Moreno Rubio', '45454545Z', 'Granada', 'Granada', 'C/Rulador B9º 2ºA', 'andres@gmail.com', '677777777');
INSERT INTO Alumno VALUES('Susana', 'Dominguez Sábado', '12231223Z', 'Granada', 'Granada', 'C/Rulador B9º 2ºA', 'susana@gmail.com', '677777777');

#Inserción de asignaturas:
INSERT INTO Asignatura VALUES ('Francés', 'A1');
INSERT INTO Asignatura VALUES ('Inglés', 'A2');
INSERT INTO Asignatura VALUES ('Alemán', 'A3');

#Inserción de grupos:
INSERT INTO Grupo VALUES ('Bachillerato', '1', 'A', 'bach1A');
INSERT INTO Grupo VALUES ('Bachillerato', '1', 'B', 'bach1B');

#Asociación de grupos a asignaturas:
INSERT INTO Tiene VALUES ('bach1A','A1'); #Al grupo bach1A se le imparte Francés.
INSERT INTO Tiene VALUES ('bach1B','A1'); #Al grupo bach1B se le imparte Francés también.

INSERT INTO Cursa VALUES('45454545Z','bach1A', 'A1');
INSERT INTO Cursa VALUES('12231223Z','bach1B', 'A1');

#El profesor con DNI yy imparte la asignatura A1.
INSERT INTO Imparte VALUES('xxxxxxxxZ','A1');
#El profesor con DNI ww imparte la asignatura A2.
INSERT INTO Imparte VALUES('xxxxxxxxY','A2');
