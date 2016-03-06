# -*- coding: utf-8 -*-
#####################################################
## DEFINICIÓN DE LA API REST del MICROSERVICIO SBD ##
#####################################################
from flask import Flask
from flask import abort
from flask import request
import jsonpickle

from APIDB.GestorAlumnosSQL import GestorAlumnos
from APIDB.GestorProfesoresSQL import GestorProfesores
from APIDB.GestorAsignaturasSQL import GestorAsignaturas
from APIDB.GestorClasesSQL import GestorClases

app = Flask(__name__)

#Activar modo verbose
v=1

############################
#   COLECCIÓN ALUMNOS      #
############################

@app.route('/alumnos',methods=['GET'])
def getAlumnos():
    '''
    Devuelve una lista de todos los estudiantes.
    curl -i -X GET localhost:8002/alumnos/
    '''
    return jsonpickle.encode(GestorAlumnos.getAlumnos())

@app.route('/alumnos',methods=['PUT'])
def putAlumnos():
    return "puting algo \n"

@app.route('/alumnos',methods=['DELETE'])
def delAlumnos():
    return "deleting algo \n"

@app.route('/alumnos',methods=['POST'])
def postAlumno():
    '''
    Método que inserta un nuevo alumno en el sistema.
    curl -d "nombre=Juan&dni=45601218Z&direccion=Calle arabl&localidad=Jerez de la frontera&provincia=Granada&fecha_nac=1988-2-6&telefono=677164459" -i -X POST localhost:8002/alumnos
    '''
    if 'dni' in request.form:
        #Presente el DNI al menos podemos grabar el alumno en el sistema.
        #Se devuelve la salida de control de
        salida = GestorAlumnos.nuevoAlumno(request.form['nombre'],
                                  request.form['dni'],
                                  request.form['direccion'],
                                  request.form['localidad'],
                                  request.form['provincia'],
                                  request.form['fecha_nac'],
                                  request.form['telefono'])
        if salida == 'OK':
            return 'OK'
        else:
            abort(404)
    else:
        abort(404)


#####################
#  ENTIDAD ALUMNO   #
#####################

@app.route('/alumnos/<string:id_alumno>',methods=['GET'])
def getAlumno(id_alumno):
    '''
    Devuelve todos los datos de un alumno buscado por su id
    en caso de existir en la base de datos.
    curl -i -X GET localhost:8002/alumnos/11223344A
    '''

    if v:
        print 'Calling GestorAlumnos.getAlumno('+id_alumno+')'

    #Si no tiene el número correcto de caracteres el identificador.
    #if len(id_alumno) != 9:
    #    abort(400)

    salida=GestorAlumnos.getAlumno(id_alumno)
    if salida=="Elemento no encontrado":
        #Enviamos el error de NotFound
        abort(404)
    else:
        return jsonpickle.encode(GestorAlumnos.getAlumno(id_alumno))

''' Hasta ver como proceder con la modificación de alumnos.
@app.route('/alumnos/<string:id_alumno>',methods=['PUT'])
def modAlumno(id_alumno):
    #Si no tiene el número correcto de caracteres el identificador.
    if len(id_alumno) != 9:
        abort(404)
    return id_alumno
'''

@app.route('/alumnos/<string:id_alumno>',methods=['DELETE'])
def delAlumno(id_alumno):
    '''
    curl -i -X DELETE localhost:8080/alumnos/11223344A
    Si el alumno no se encuentra se devuelve: "Elemento no encontrado".

    Si la solicitud se realiza con un identificador de alumno que
    no cumple con ciertos requisitos como la longitud = 9, se devuelve
    el error 400 - Bad request, que significa que la solicitud contiene
    sintaxis errónea y no debería repetirse.

    Si la solicitud tiene la sintaxis correcta pero no existe el recurso
    el error es el 404 - Not found, significa recurso no encontrado,
    identificia que el servidor no ha encontrado el recurso solicitado.

    '''
    #if len(id_alumno) != 9:
    #    abort(400)

    salida = GestorAlumnos.delAlumno(id_alumno)
    if salida=="Elemento no encontrado":
        abort(404)
    else:
        return 'Elemento eliminado'

@app.route('/alumnos/<string:id_alumno>/profesores',methods=['GET'])
def getProfesoresAlumno(id_alumno):
    '''
    curl -i -X GET localhost:8080/alumnos/1/profesores
    '''
    return jsonpickle.encode(GestorAlumnos.getProfesores(id_alumno))

@app.route('/alumnos/<string:id_alumno>/asignaturas',methods=['GET'])
def getAsignaturasAlumno(id_alumno):
    '''
    curl -i -X GET localhost:8080/alumnos/1/asignaturas
    '''
    return jsonpickle.encode(GestorAlumnos.getAsignaturas(id_alumno))

@app.route('/alumnos/<string:id_alumno>/clases',methods=['GET'])
def getClasesAlumnos(id_alumno):
    '''
    Devuelve las clases a en las que está matriculado el alumno, como 1AESO o 2CBACH.
    curl -i -X GET localhost:8080/alumnos/1/clases
    '''
    return jsonpickle.encode(GestorAlumnos.getClases(id_alumno))


###############################
#   COLECCIÓN PROFESORES      #
###############################

@app.route('/profesores',methods=['GET'])
def getProfesores():
    '''
    Devuelve una lista con todos los profesores registrados en el sistema.
    > curl -i -X GET localhost:8002/profesores
    '''
    return jsonpickle.encode(GestorProfesores.getProfesores())

@app.route('/profesores',methods=['PUT'])
def putProfesores():
    return "puting algo \n"

@app.route('/profesores',methods=['DELETE'])
def delProfesores():
    return "deleting algo \n"

@app.route('/profesores',methods=['POST'])
def postProfesor():
    '''
    Método que inserta un nuevo alumno en el sistema.
    curl -d "nombre=Juan&dni=45601218Z&direccion=Calle arabl&localidad=Jerez de la frontera&provincia=Granada&fecha_nac=1988-2-6&telefonoA=277164459&telefonoB=177164459" -i -X POST localhost:8080/profesores
    '''
    if 'dni' in request.form:
        salida = GestorProfesores.nuevoProfesor(request.form['nombre'],
                                  request.form['dni'],
                                  request.form['direccion'],
                                  request.form['localidad'],
                                  request.form['provincia'],
                                  request.form['fecha_nac'],
                                  request.form['telefonoA'],
                                  request.form['telefonoB'])
        if salida == 'OK':
            return 'OK'
        else:
            abort(404)
    else:
        abort(404)


#######################
#   ENTIDAD PROFESOR  #
#######################

@app.route('/profesores/<string:id_profesor>',methods=['GET'])
def getProfesor(id_profesor):
    '''
    Devuelve todos los datos de un alumno buscado por su id
    en caso de existir en la base de datos.
    curl -i -X GET localhost:8080/profesores/11223344A

    '''
    #Si no tiene el número correcto de caracteres el identificador.
    if len(id_profesor) != 9:
        abort(400)

    salida=GestorProfesores.getProfesor(id_profesor)
    if salida=="Elemento no encontrado":
        #Enviamos el error de NotFound
        abort(404)
    else:
        return jsonpickle.encode(GestorProfesores.getProfesor(id_profesor))

''' Hasta ver como proceder con la modificación de profesores.
@app.route('/profesores/<string:id_profesor>',methods=['PUT'])
def modProfesor(id_profesor):
    #Si no tiene el número correcto de caracteres el identificador.
    if len(id_profesor) != 9:
        abort(404)
    return id_profesor
'''

@app.route('/profesores/<string:id_profesor>',methods=['DELETE'])
def delProfesor(id_profesor):
    '''
    curl -i -X DELETE localhost:8080/profesores/11223344A
    Si el alumno no se encuentra se devuelve: "Elemento no encontrado".

    Si la solicitud se realiza con un identificador de alumno que
    no cumple con ciertos requisitos como la longitud = 9, se devuelve
    el error 400 - Bad request, que significa que la solicitud contiene
    sintaxis errónea y no debería repetirse.

    Si la solicitud tiene la sintaxis correcta pero no existe el recurso
    el error es el 404 - Not found, significa recurso no encontrado,
    identificia que el servidor no ha encontrado el recurso solicitado.

    '''
    if len(id_profesor) != 9:
        abort(400)

    salida = GestorProfesores.delProfesor(id_profesor)
    if salida=="Elemento no encontrado":
        abort(404)
    else:
        return 'Elemento eliminado'

@app.route('/profesores/<string:id_profesor>/alumnos',methods=['GET'])
def getAlumnosProfesor(id_profesor):
    '''
    curl -i -X GET localhost:8080/profesores/1/alumnos
    '''
    return jsonpickle.encode(GestorProfesores.getAlumnos(id_profesor))

@app.route('/profesores/<string:id_profesor>/asignaturas',methods=['GET'])
def getAsignaturasProfesor(id_profesor):
    '''
    curl -i -X GET localhost:8080/profesores/1/asignaturas
    '''
    return jsonpickle.encode(GestorProfesores.getAsignaturas(id_profesor))

@app.route('/profesores/<string:id_profesor>/clases',methods=['GET'])
def getCursosProfesor(id_profesor):
    '''
    curl -i -X GET localhost:8080/profesores/1/clases
    '''
    return jsonpickle.encode(GestorProfesores.getCursos(id_profesor))



############################
#   COLECCIÓN ASIGNATURAS  #
############################


@app.route('/asignaturas',methods=['GET'])
def getAsignaturas():
    '''
    Devuelve una lista con todos las asignaturas registradas en el sistema.
    > curl -i -X GET localhost:8002/asignaturas
    '''
    return jsonpickle.encode(GestorAsignaturas.getAsignaturas())


@app.route('/asignaturas',methods=['POST'])
def postAsignatura():
    '''
    Inserta una nueva asignatura en el sistema.
    curl -d "id=" -i -X POST localhost:8080/asignaturas
    '''
    if 'id' in request.form:
        salida = GestorAsignaturas.nuevaAsignatura(request.form['id'],request.form['nombre'])
        if salida == 'OK':
            return 'OK'
        else:
            abort(404)
    else:
        abort(404)


#########################
#   ENTIDAD ASIGNATURA  #
#########################

@app.route('/asignaturas/<string:id_asignatura>',methods=['GET'])
def getAsignatura(id_asignatura):
    '''
    Devuelve todos los datos de una asignatura buscado por su id
    en caso de existir en la base de datos.
    curl -i -X GET localhost:8002/asignaturas/ln

    '''

    salida=GestorAsignaturas.getAsignatura(id_asignatura)
    if salida=="Elemento no encontrado":
        #Enviamos el error de NotFound
        abort(404)
    else:
        return jsonpickle.encode(salida)

@app.route('/asignaturas/<string:id_asignatura>',methods=['DELETE'])
def delAsignatura(id_asignatura):
    '''
    Elimina la asignatura que se especifica con el identificador pasado, en caso de exisitir en el sistema.
    curl -i -X DELETE localhost:8002/asignaturas/ln
    '''
    if len(id_asignatura) != 2:
        abort(400)

    salida = GestorAsignaturas.delAsignatura(id_asignatura)
    if salida=="Elemento no encontrado":
        abort(404)
    else:
        return 'Elemento eliminado\n'

@app.route('/asignaturas/<string:id_asignatura>/alumnos',methods=['GET'])
def getAlumnosAsignatura(id_asignatura):
    '''
    curl -i -X GET localhost:8002/asignaturas/fr/alumnos
    '''
    return jsonpickle.encode(GestorAsignaturas.getAlumnos(id_asignatura))

@app.route('/asignaturas/<string:id_asignatura>/profesores', methods=['GET'])
def getProfesoresAsignatura(id_asignatura):
    '''
    Devuelve una lista con los profesores que imparten clase en una asignatura
    curl -i -X GET localhost:8002/asignaturas/fr/profesores
    '''
    return jsonpickle.encode(GestorAsignaturas.getProfesores(id_asignatura))

@app.route('/asignaturas/<string:id_asignatura>/clases',methods=['GET'])
def getCursosAsignaturas(id_asignatura):
    '''
    Devuelve una lista con los clases en los que se imparte esa asignatura.
    curl -i -X GET localhost:8002/asignaturas/fr/clases
    '''
    return jsonpickle.encode(GestorAsignaturas.getCursos(id_asignatura))




############################
#   COLECCIÓN CLASES       #
############################


@app.route('/clases',methods=['GET'])
def getCursos():
    '''
    Devuelve una lista con todos los clases registradas en el sistema.
    > curl -i -X GET localhost:8002/clases
    '''
    return jsonpickle.encode(GestorClases.getClases())


@app.route('/clases',methods=['POST'])
def postCurso():
    '''
    Inserta una nueva clase en el sistema.
    curl -d "id=" -i -X POST localhost:8002/clases
    '''
    if 'id' in request.form:
        salida = GestorClases.nuevoCurso(request.form['id'],request.form['curso'], request.form['grupo'], request.form['nivel'])
        if salida == 'OK':
            return 'OK'
        else:
            abort(404)
    else:
        abort(404)


#########################
#   ENTIDAD CLASE       #
#########################

@app.route('/clases/<string:id_clase>',methods=['GET'])
def getCurso(id_curso):
    '''
    Devuelve toda la información sobre el curso que se pasa el id.
    curl -i -X GET localhost:8002/clases/ln

    '''

    salida=GestorClases.getClase(id_curso)
    if salida=="Elemento no encontrado":
        #Enviamos el error de NotFound
        abort(404)
    else:
        return jsonpickle.encode(salida)


@app.route('/clases/<string:id_clase>/alumnos',methods=['GET'])
def getAlumnosCurso(id_curso):
    '''
    Devuelve todos los alumnos que se encuentran matriculados en ese curso.
    curl -i -X GET localhost:8002/clases/fr/alumnos
    '''
    return jsonpickle.encode(GestorClases.getAlumnos(id_curso))


@app.route('/clases/<string:id_clase>/profesores', methods=['GET'])
def getProfesoresCurso(id_curso):
    '''
    Devuelve una lista con los profesores que imparten clase a un grupo
    curl -i -X GET localhost:8002/curso/1ESOA/profesores
    '''
    return jsonpickle.encode(GestorClases.getProfesores(id_curso))

@app.route('/clases/<string:id_curso>/asignaturas', methods=['GET'])
def getAsignaturasCurso(id_curso):
    '''
    Devuelve una lista con las asignaturas que se imparten a un curso.
    curl -i -X GET localhost:8002/curso/1ESOA/asignaturas
    '''
    return jsonpickle.encode(GestorClases.getAsignaturas(id_curso))



if __name__ == '__main__':
    app.run(debug=True)
