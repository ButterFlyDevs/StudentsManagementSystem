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
from APIDB.GestorMatriculasSQL import GestorMatriculas
from APIDB.GestorImpartesSQL import GestorImpartes
from APIDB.GestorAsociacionesSQL import GestorAsociaciones

app = Flask(__name__)

#Activar modo verbose
v=1
nombreMicroservicio = '\n## Microservicio BD ##\n'

############################
#   COLECCIÓN ALUMNOS      #
############################

@app.route('/alumnos',methods=['GET'])
def getAlumnos():
    '''
    Devuelve una lista de todos los estudiantes.
    curl -i -X GET localhost:8002/alumnos
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
    if v:
        print nombreMicroservicio
        print 'Recurso: /alumnos , metodo: POST'
        print "Petición: "
        print request.form


    salida = GestorAlumnos.nuevoAlumno(request.form['nombre'],
                              request.form['apellidos'],
                              request.form['dni'],
                              request.form['direccion'],
                              request.form['localidad'],
                              request.form['provincia'],
                              request.form['fecha_nacimiento'],
                              request.form['telefono'])
    if salida == 'OK':
        return 'OK'
    else:
        return salida
        #abort(404)



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
        #return jsonpickle.encode(GestorAlumnos.getAlumno(id_alumno), unpicklable=False)
        return jsonpickle.encode(salida, unpicklable=False)

@app.route('/alumnos/<string:id_alumno>',methods=['POST'])
def modAlumno(id_alumno):
    '''
    Función que modifica los atributos de un alumno dado su identificación, usando la función
    modAlumnoCompleto de la APIDB
    curl -d "nombre=Pedro&apellidos=Torrssr&dni=234242&direccion=Calle Duqesa&locia=Granada&fecha_nacimiento=1988-12-4&telefono=23287282" -i -X POST localhost:8002/alumnos/1
    '''
    if v:
        print 'Calling GestorAlumnos.modAlumnoCompleto()'

    #El id del alumno se pasa por la URL
    salida = GestorAlumnos.modAlumnoCompleto(id_alumno,
                                             request.form['nombre'],
                                             request.form['apellidos'],
                                             request.form['dni'],
                                             request.form['direccion'],
                                             request.form['localidad'],
                                             request.form['provincia'],
                                             request.form['fecha_nacimiento'],
                                             request.form['telefono']
                                            );

    if v:
        print "SALIDA: "+str(salida)

    if salida == 'OK':
        return 'OK'
    else:
        return salida

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
    Devuelve todos los profesores que imparten clase a ese alumno.
    curl -i -X GET localhost:8002/alumnos/1/profesores
    '''
    return jsonpickle.encode(GestorAlumnos.getProfesores(id_alumno))

@app.route('/alumnos/<string:id_alumno>/asignaturas',methods=['GET'])
def getAsignaturasAlumno(id_alumno):
    '''
    curl -i -X GET localhost:8002/alumnos/1/asignaturas
    '''
    return jsonpickle.encode(GestorAlumnos.getAsignaturas(id_alumno))

@app.route('/alumnos/<string:id_alumno>/clases',methods=['GET'])
def getClasesAlumnos(id_alumno):
    '''
    Devuelve las clases a en las que está matriculado el alumno, como 1AESO o 2CBACH.
    curl -i -X GET localhost:8002/alumnos/1/clases
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
    if v:
        print "## Microservicio DB ##"
        print 'Calling GestorPRofesores.getAlumnos()'
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
    Método que inserta un nuevo profesor en el sistema.
    curl -d "nombre=Juan&apellidos=Bartlo&dni=46666&direccion=Calle arabl&localidad=Jerez de la fronta&provincia=Granada&fecha_nacimiento=1988-2-6&telefono=137631" -i -X POST localhost:8002/profesores


    '''
    if v:
        print "Calling postProfesor()"
        print str(request.form)

    salida = GestorProfesores.nuevoProfesor(request.form['nombre'],
                              request.form['apellidos'],
                              request.form['dni'],
                              request.form['direccion'],
                              request.form['localidad'],
                              request.form['provincia'],
                              request.form['fecha_nacimiento'],
                              request.form['telefono'],
                              )
    if salida == 'OK':
        return 'OK'
    else:
        #abort(404)
        return salida


#######################
#   ENTIDAD PROFESOR  #
#######################

@app.route('/profesores/<string:id_profesor>',methods=['GET'])
def getProfesor(id_profesor):
    '''
    Devuelve todos los datos de un alumno buscado por su id
    en caso de existir en la base de datos.
    curl -i -X GET localhost:8002/profesores/11223344A

    '''

    salida=GestorProfesores.getProfesor(id_profesor)
    if salida=="Elemento no encontrado":
        #Enviamos el error de NotFound
        abort(404)
    else:
        return jsonpickle.encode(GestorProfesores.getProfesor(id_profesor), unpicklable=False)

@app.route('/profesores/<string:id_profesor>',methods=['POST'])
def modProfesorCompleto(id_profesor):
    '''
    Función que modifica los atributos de un profesor dado su identificación, usando la función
    modProfesorCompleto de la APIDB
    curl -d "nombre=Pedro&apellidos=Torrssr&dni=234242&direccion=Calle Duqesa&localidad=Granada&proviia=Burgos&fecha_nacimiento=1988-12-4&telefono=23287282" -i -X POST localhost:8002/profesores/1

    '''
    if v:
        print 'Calling GestorProfesores.modProfesorCompleto()'

    #El id del alumno se pasa por la URL
    salida = GestorProfesores.modProfesorCompleto(id_profesor,
                                             request.form['nombre'],
                                             request.form['apellidos'],
                                             request.form['dni'],
                                             request.form['direccion'],
                                             request.form['localidad'],
                                             request.form['provincia'],
                                             request.form['fecha_nacimiento'],
                                             request.form['telefono']
                                            );

    if v:
        print "SALIDA: "+str(salida)

    if salida == 'OK':
        return 'OK'
    else:
        return salida

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

#Métodos que relacionan con otras entidades.

@app.route('/profesores/<string:id_profesor>/alumnos',methods=['GET'])
def getAlumnosProfesor(id_profesor):
    '''
    curl -i -X GET localhost:8002/profesores/1/alumnos
    '''
    return jsonpickle.encode(GestorProfesores.getAlumnos(id_profesor))

@app.route('/profesores/<string:id_profesor>/asignaturas',methods=['GET'])
def getAsignaturasProfesor(id_profesor):
    '''
    curl -i -X GET localhost:8002/profesores/1/asignaturas
    '''
    return jsonpickle.encode(GestorProfesores.getAsignaturas(id_profesor))

@app.route('/profesores/<string:id_profesor>/clases',methods=['GET'])
def getClasesProfesor(id_profesor):
    '''
    curl -i -X GET localhost:8002/profesores/1/clases
    '''
    return jsonpickle.encode(GestorProfesores.getClases(id_profesor))



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
    curl -d "nombre=ComputacionZZ" -i -X POST localhost:8002/asignaturas
    '''
    salida = GestorAsignaturas.nuevaAsignatura(request.form['nombre'])
    if salida == 'OK':
        return 'OK'
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
    curl -i -X GET localhost:8002/asignaturas/1

    '''

    salida=GestorAsignaturas.getAsignatura(id_asignatura)
    if salida=="Elemento no encontrado":
        #Enviamos el error de NotFound
        abort(404)
    else:
        return jsonpickle.encode(salida)

@app.route('/asignaturas/<string:id_asignatura>',methods=['POST'])
def modAsignaturaCompleta(id_asignatura):
    '''
    Función que modifica los atributos de una asignatura completa dado su identificación
    curl -d "nombre=Ciudadania" -i -X POST localhost:8002/asignaturas/1

    '''
    if v:
        print 'Calling GestorProfesores.modProfesorCompleto()'

    #El id del alumno se pasa por la URL
    salida = GestorAsignaturas.modAsignaturaCompleta(id_asignatura, request.form['nombre']);

    if v:
        print "SALIDA: "+str(salida)

    if salida == 'OK':
        return 'OK'
    else:
        return salida


@app.route('/asignaturas/<string:id_asignatura>',methods=['DELETE'])
def delAsignatura(id_asignatura):
    '''
    Elimina la asignatura que se especifica con el identificador pasado, en caso de exisitir en el sistema.
    curl -i -X DELETE localhost:8002/asignaturas/ln
    '''


    salida = GestorAsignaturas.delAsignatura(id_asignatura)
    if salida=="Elemento no encontrado":
        abort(404)
    else:
        return str(salida)

#Métodos que relacionan con otras entidades

@app.route('/asignaturas/<string:id_asignatura>/alumnos',methods=['GET'])
def getAlumnosAsignatura(id_asignatura):
    '''
    curl -i -X GET localhost:8002/asignaturas/1/alumnos
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
def getClasesAsignaturas(id_asignatura):
    '''
    Devuelve una lista con los clases en los que se imparte esa asignatura.
    curl -i -X GET localhost:8002/asignaturas/1/clases
    '''
    return jsonpickle.encode(GestorAsignaturas.getClases(id_asignatura))




############################
#   COLECCIÓN CLASES       #
############################


@app.route('/clases',methods=['GET'])
def getClases():
    '''
    Devuelve una lista con todos los clases registradas en el sistema.
    > curl -i -X GET localhost:8002/clases
    '''
    return jsonpickle.encode(GestorClases.getClases())

@app.route('/clases',methods=['POST'])
def postClase():
    '''
    Inserta una nueva clase en el sistema.
    curl -d "curso=3&grupo=C&nivel=ESO" -i -X POST localhost:8002/clases
    '''
    salida = GestorClases.nuevaClase(request.form['curso'], request.form['grupo'], request.form['nivel'])
    if salida == 'OK':
        return 'OK'
    else:
        abort(404)

#########################
#   ENTIDAD CLASE       #
#########################

@app.route('/clases/<string:id_clase>',methods=['GET'])
def getClase(id_clase):
    '''
    Devuelve toda la información sobre la clase que se pasa el id.
    curl -i -X GET localhost:8002/clases/1
    '''
    salida=GestorClases.getClase(id_clase)
    if salida=="Elemento no encontrado":
        #Enviamos el error de NotFound
        abort(404)
    else:
        return jsonpickle.encode(salida)

@app.route('/clases/<string:id_clase>',methods=['DELETE'])
def delClase(id_clase):
    '''
    Elimina la clase que se especifica con el identificador pasado, en caso de exisitir en el sistema.
    curl -i -X DELETE localhost:8002/clases/1
    '''
    salida = GestorClases.delClase(id_clase)
    if salida=="Elemento no encontrado":
        abort(404)
    else:
        return str(salida)

#Métodos que relacionan con otras entidades

@app.route('/clases/<string:id_clase>/alumnos',methods=['GET'])
def getAlumnosClase(id_clase):
    '''
    Devuelve todos los alumnos que se encuentran matriculados en ese curso.
    curl -i -X GET localhost:8002/clases/1/alumnos
    '''
    return jsonpickle.encode(GestorClases.getAlumnos(id_clase))

@app.route('/clases/<string:id_clase>/profesores', methods=['GET'])
def getProfesoresClase(id_clase):
    '''
    Devuelve una lista con los profesores que imparten clase a un grupo
    curl -i -X GET localhost:8002/clases/1/profesores
    '''
    return jsonpickle.encode(GestorClases.getProfesores(id_clase))

@app.route('/clases/<string:id_clase>/asignaturas', methods=['GET'])
def getAsignaturasClase(id_clase):
    '''
    Devuelve una lista con las asignaturas que se imparten a una clase concreta.
    curl -i -X GET localhost:8002/clases/1/asignaturas
    '''
    return jsonpickle.encode(GestorClases.getAsignaturas(id_clase))


@app.route('/clases/<string:id_clase>/asociaciones', methods=['GET'])
def getAsociacionesClase(id_clase):
    '''
    Devuelve una lista con las asociaciones de clase-asignatura que se imparten a una clase concreta.
    Estas entindades son distintas de las asignaturas que se imparten en las clases ya que estas nos llevan a las
    asignaturas en general y las asociaciones son una especificación de la asignatura para una clase concreta.

    curl -i -X GET localhost:8002/clases/1/asociaciones

    '''
    return jsonpickle.encode(GestorClases.getAsociaciones(id_clase))






############################
#   COLECCIÓN MATRICULAS       #
############################


@app.route('/matriculas',methods=['GET'])
def getMatriculas():
    '''
    Devuelve una lista con todos las matriculas registradas en el sistema.
    curl -i -X GET localhost:8002/matriculas
    '''
    return jsonpickle.encode(GestorMatriculas.getMatriculas())

@app.route('/matriculas',methods=['POST'])
def postMatricula():
    '''
    Inserta una nueva matricula en el sistema.
    curl -d "id_alumno=1&id_asociacion=2" -i -X POST localhost:8002/matriculas
    '''
    salida = GestorMatriculas.nuevaMatricula(request.form['id_alumno'], request.form['id_asociacion'])
    if salida == 'OK':
        return 'OK'
    else:
        print salida
        abort(404)

@app.route('/matriculas/<string:id_matricula>',methods=['DELETE'])
def delMatricula(id_matricula):
    '''
    Elimina la matricula que se especifica con el identificador pasado, en caso de exisitir en el sistema.
    curl -i -X DELETE localhost:8002/matriculas/1
    '''
    salida = GestorMatriculas.delMatricula(id_matricula)
    if salida=="Elemento no encontrado":
        abort(404)
    else:
        return str(salida)



############################
#   COLECCIÓN IMPARTES     #
############################


@app.route('/impartes',methods=['GET'])
def getImpartes():
    '''
    Devuelve una lista con todos las tuplas de la tabla Imparte de la BD.
    curl -i -X GET localhost:8002/impartes
    '''
    return jsonpickle.encode(GestorImpartes.getImpartes())

@app.route('/impartes',methods=['POST'])
def insertarImparte():
    '''
    Inserta una nueva relación imparte en el sistema, un profesor que imparte clase en una asocaición asignatura-clase, ejempo; Juan -> Lengua-4ºC-ESO
    curl -d "id_asociacion=2&id_profesor=1" -i -X POST localhost:8002/impartes
    '''
    salida = GestorImpartes.nuevoImparte(request.form['id_asociacion'], request.form['id_profesor'])
    if salida == 'OK':
        return 'OK'
    else:
        print salida
        abort(404)

@app.route('/impartes/<string:id_imparte>',methods=['DELETE'])
def delImparte(id_imparte):
    '''
    Elimina la matricula que se especifica con el identificador pasado, en caso de exisitir en el sistema.
    curl -i -X DELETE localhost:8002/impartes/1
    '''
    salida = GestorImpartes.delImparte(id_imparte)
    if salida=="Elemento no encontrado":
        abort(404)
    else:
        return str(salida)



#############################
#   COLECCIÓN ASOCIACIONES  #
#############################


@app.route('/asociaciones',methods=['GET'])
def getAsociaciones():
    '''
    Devuelve una lista con todos las tuplas de la tabla Asocia de la BD.
    curl -i -X GET localhost:8002/asociaciones
    '''
    return jsonpickle.encode(GestorAsociaciones.getAsociaciones())

@app.route('/asociaciones/<string:id_asociacion>', methods=['GET'])
def getTodoSobreAsociacion(id_asociacion):
    '''
    Devuelve todos los datos importates de una asociacione (una asignatura que se da a una clase en concreto) tal como
    su nombre completo, nombre del profesor y nombre de los alumnos.

    curl -i -X GET localhost:8002/asociaciones/1

    En lugar de hacer tres llamadas a métodos sueltos de la colección asociación para que nos de su nombre legible,
    el profesor que la imparte y los alumnos matriculados creamos un método que nos devuelve la información al completo.
    '''

    #Creamos un pequeño objeto que represente la asociacion con su máxima información
    class AsociacionCompleta:
        nombreAsignatura = ""
        profesoresAsociacion = []
        alumnosAsociacion = []

    asociacion = AsociacionCompleta()

    #Nombre de la asignatura de la asociacion
    asociacion.nombreAsignatura = GestorAsociaciones.getAsociacionCompleta(id_asociacion).nombreAsignatura;
    #Profesor que imparte la asociación:
    asociacion.profesoresAsociacion = GestorAsociaciones.getProfesores(id_asociacion);
    #Alumnos que están matriculados a esa asociacion de asignatura y clase concreta (BASE DEL SISTEMA).
    asociacion.alumnosAsociacion = GestorAsociaciones.getAlumnos(id_asociacion);

    return jsonpickle.encode(asociacion)


@app.route('/asociaciones',methods=['POST'])
def postAsociacion():
    '''
    Inserta una nueva relación imparte en el sistema.
    curl -d "id_asignatura=2&id_clase=3" -i -X POST localhost:8002/asociaciones
    '''
    salida = GestorAsociaciones.nuevaAsociacion(request.form['id_clase'], request.form['id_asignatura'])
    print salida
    if salida == 'OK':
        return 'OK'
    else:
        print salida
        #abort(404)
        return salida

@app.route('/asociaciones/<string:id_asociacion>',methods=['DELETE'])
def delAsociacion(id_asociacion):
    '''
    Elimina la asociacion entre clase y aseignatua que se especifica con el identificador pasado, en caso de exisitir en el sistema.
    curl -i -X DELETE localhost:8002/asociaciones/1
    '''
    salida = GestorAsociaciones.delAsociacion(id_asociacion)
    print salida
    if salida=="Elemento no encontrado":
        abort(404)
    else:
        return str(salida)



if __name__ == '__main__':
    app.run(debug=True)
