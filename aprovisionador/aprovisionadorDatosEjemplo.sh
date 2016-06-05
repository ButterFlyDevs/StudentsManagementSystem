#!/bin/bash

#Fichero que aprovisiona el sistema con datos de muestra para comprobar su funcionamiento y extender funcionalidad.
#Atención, este fichero deberá ser modificado cuando se modifique algo en el sistema para que no pierda funcionalidad.

##### Aprovisionador que sólo hace uso de la APIG para su interacción con el sistema ####

cat << "EOF"
 ▄▄▄▄▄▄▄▄▄▄▄  ▄▄       ▄▄  ▄▄▄▄▄▄▄▄▄▄▄
▐░░░░░░░░░░░▌▐░░▌     ▐░░▌▐░░░░░░░░░░░▌
▐░█▀▀▀▀▀▀▀▀▀ ▐░▌░▌   ▐░▐░▌▐░█▀▀▀▀▀▀▀▀▀
▐░█▄▄▄▄▄▄▄▄▄ ▐░▌ ▐░▐░▌ ▐░▌▐░█▄▄▄▄▄▄▄▄▄
▐░░░░░░░░░░░▌▐░▌  ▐░▌  ▐░▌▐░░░░░░░░░░░▌
 ▀▀▀▀▀▀▀▀▀█░▌▐░▌   ▀   ▐░▌ ▀▀▀▀▀▀▀▀▀█░▌
 ▄▄▄▄▄▄▄▄▄█░▌▐░▌       ▐░▌ ▄▄▄▄▄▄▄▄▄█░▌
▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌
 ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀
EOF
echo -e "\n### Aprovisionador de datos de muestra del sistema ###\n"

echo -e "\n### Reseteando Base de Datos en microSBD ###\n"
mysql -u root -p'root' < ../SMS-Back-End/sbd/APIDB/DBCreatorv1.sql

sleep 3

#Insercción de 6 alumnos

#Alumno A
echo -e "\nInsertando Alumno A"
curl -d "nombre=nombreA&apellidos=ApellidosB&dni=11111111&direccion=calleA&localidad=localidadA\
&provincia=provinciaA&fecha_nacimiento=1900-1-1&telefono=111111111" \
--data-urlencode 'imagen='"$( base64 jake.jpg)"''  -X POST -G localhost:8001/_ah/api/helloworld/v1/alumnos/insertarAlumno2

#Alumno B
echo -e "\nInsertando Alumno B"
curl -d "nombre=nombreB&apellidos=ApellidosB&dni=22222222&direccion=calleB&localidad=localidadB\
&provincia=provinciaB&fecha_nacimiento=1900-1-1&telefono=222222222" \
--data-urlencode 'imagen='"$( base64 finn.jpg)"''  -X POST -G localhost:8001/_ah/api/helloworld/v1/alumnos/insertarAlumno2

#Alumno C
echo -e "\nInsertando Alumno C"
curl -d "nombre=nombreC&apellidos=ApellidosC&dni=33333333&direccion=calleC&localidad=localidadC\
&provincia=provinciaC&fecha_nacimiento=1900-1-1&telefono=333333333" \
--data-urlencode 'imagen='"$( base64 rigby.jpg)"''  -X POST -G localhost:8001/_ah/api/helloworld/v1/alumnos/insertarAlumno2

#Alumno D
echo -e "\nInsertando Alumno D"
curl -d "nombre=nombreD&apellidos=ApellidosD&dni=44444444&direccion=calleD&localidad=localidadD\
&provincia=provinciaD&fecha_nacimiento=1900-1-1&telefono=444444444" \
--data-urlencode 'imagen='"$( base64 mordecai.jpg)"''  -X POST -G localhost:8001/_ah/api/helloworld/v1/alumnos/insertarAlumno2

#Alumno E
echo -e "\nInsertando Alumno E"
curl -d "nombre=nombreE&apellidos=ApellidosE&dni=55555555&direccion=calleE&localidad=localidadE\
&provincia=provinciaE&fecha_nacimiento=1900-1-1&telefono=555555555" \
--data-urlencode 'imagen='"$( base64 bob.jpg)"''  -X POST -G localhost:8001/_ah/api/helloworld/v1/alumnos/insertarAlumno2

#Alumno F
echo -e "\nInsertando Alumno F"
curl -d "nombre=nombreF&apellidos=ApellidosF&dni=66666666&direccion=calleF&localidad=localidadF\
&provincia=provinciaF&fecha_nacimiento=1900-1-1&telefono=666666666" \
--data-urlencode 'imagen='"$( base64 desdentado.jpg)"''  -X POST -G localhost:8001/_ah/api/helloworld/v1/alumnos/insertarAlumno2

#Insertando 3 Profesores

#Profesor A
echo -e "\nInsertando Profesor A"
curl -d "nombre=nombreProfesorA&apellidos=apellidoProfesorA&dni=11111111&direccion=calleProfesorA&localidad=localidadProfesorA&\
provincia=provinciaProfesorA&fecha_nacimiento=1900-1-1&telefono=111111111" \
-X POST -G localhost:8001/_ah/api/helloworld/v1/profesores/insertarProfesor

#Profesor B
echo -e "\nInsertando Profesor B"
curl -d "nombre=nombreProfesorB&apellidos=apellidoProfesorB&dni=22222222&direccion=calleProfesorB&localidad=localidadProfesorB&\
provincia=provinciaProfesorB&fecha_nacimiento=1900-1-1&telefono=222222222" \
-X POST -G localhost:8001/_ah/api/helloworld/v1/profesores/insertarProfesor

#Profesor C
echo -e "\nInsertando Profesor C"
curl -d "nombre=nombreProfesorC&apellidos=apellidoProfesorC&dni=33333333&direccion=calleProfesorC&localidad=localidadProfesorC&\
provincia=provinciaProfesorC&fecha_nacimiento=1900-1-1&telefono=333333333" \
-X POST -G localhost:8001/_ah/api/helloworld/v1/profesores/insertarProfesor

#Insertamos 3 clases

#Clase A
echo -e "\nInsertando Clase A"
curl  -d "curso=1&grupo=A&nivel=Primaria" -X POST -G localhost:8001/_ah/api/helloworld/v1/clases/insertarClase

#Clase B
echo -e "\nInsertando Clase B"
curl -d "curso=1&grupo=B&nivel=Primaria" -X POST -G localhost:8001/_ah/api/helloworld/v1/clases/insertarClase

#Clase C
echo -e "\nInsertando Clase C"
curl -d "curso=1&grupo=C&nivel=Primaria" -X POST -G localhost:8001/_ah/api/helloworld/v1/clases/insertarClase

#Insertamos 3 asignaturas

#Asignatura A
echo -e "\nInsertando Asignatura A"
curl -d "nombre=AsignaturaA" -X POST -G localhost:8001/_ah/api/helloworld/v1/asignaturas/insertarAsignatura

#Asignatura B
echo -e "\nInsertando Asignatura B"
curl -d "nombre=AsignaturaB" -X POST -G localhost:8001/_ah/api/helloworld/v1/asignaturas/insertarAsignatura

#Asignatura C
echo -e "\nInsertando Asignatura C"
curl -d "nombre=AsignaturaC" -X POST -G localhost:8001/_ah/api/helloworld/v1/asignaturas/insertarAsignatura


### Asociaciones ###
#Relacionamos las clases con las asignaturas#

# Asignatura1->clase1
echo -e "\nAsociando aisgnatura 1 a clase 1"
curl -d "id_asignatura=1&id_clase=1" -X POST -G localhost:8001/_ah/api/helloworld/v1/asociaciones/insertaAsociacion

# Asignatura2->clase2
echo -e "\nAsociando aisgnatura 2 a clase 2"
curl -d "id_asignatura=2&id_clase=2" -X POST -G localhost:8001/_ah/api/helloworld/v1/asociaciones/insertaAsociacion

# Asignatura3->clase3
echo -e "\nAsociando aisgnatura 3 a clase 3"
curl -d "id_asignatura=3&id_clase=3" -X POST -G localhost:8001/_ah/api/helloworld/v1/asociaciones/insertaAsociacion

## Matriculando alumnos a las asocaiciones ##
#Matriculamos dos alumnos a cada asociación, ejem: alumnoA-> (asignaturaA-1ºAPrimaria)

# Alumno1->asocaicion1
echo -e "\nMatriculando alumno1 en asociacion 1"
curl -d "id_alumno=1&id_asociacion=1" -X POST -G localhost:8001/_ah/api/helloworld/v1/matriculas/insertarMatricula

# Alumno2->asocaicion1
echo -e "\nMatriculando alumno2 en asociacion 1"
curl -d "id_alumno=2&id_asociacion=1" -X POST -G localhost:8001/_ah/api/helloworld/v1/matriculas/insertarMatricula

# Alumno3->asocaicion2
echo -e "\nMatriculando alumno3 en asociacion 2"
curl -d "id_alumno=3&id_asociacion=2" -X POST -G localhost:8001/_ah/api/helloworld/v1/matriculas/insertarMatricula

# Alumno4->asocaicion2
echo -e "\nMatriculando alumno4 en asociacion 2"
curl -d "id_alumno=4&id_asociacion=2" -X POST -G localhost:8001/_ah/api/helloworld/v1/matriculas/insertarMatricula

# Alumno5->asocaicion3
echo -e "\nMatriculando alumno5 en asociacion 3"
curl -d "id_alumno=3&id_asociacion=3" -X POST -G localhost:8001/_ah/api/helloworld/v1/matriculas/insertarMatricula

# Alumno6->asocaicion3
echo -e "\nMatriculando alumno6 en asociacion 3"
curl -d "id_alumno=6&id_asociacion=3" -X POST -G localhost:8001/_ah/api/helloworld/v1/matriculas/insertarMatricula

## Asignando profesores a las asocaiciones ##
#Asignamos un profesor a cada asociación, ejem: profesorA-> (asignaturaA-1ºAPrimaria)

# Profesor1->asocaicion1
echo -e "\nAsignando profesor1 en asociacion 1"
curl -d "id_asociacion=1&id_profesor=1" -X POST -G localhost:8001/_ah/api/helloworld/v1/impartes/insertarImparte

# Profesor2->asocaicion2
echo -e "\nAsignando profesor2 en asociacion 2"
curl -d "id_asociacion=2&id_profesor=2" -X POST -G localhost:8001/_ah/api/helloworld/v1/impartes/insertarImparte

# Profesor3->asocaicion3
echo -e "\nAsignando profesor3 en asociacion 3"
curl -d "id_asociacion=3&id_profesor=3" -X POST -G localhost:8001/_ah/api/helloworld/v1/impartes/insertarImparte
