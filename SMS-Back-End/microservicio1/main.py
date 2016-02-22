# -*- coding: utf-8 -*-
from flask import Flask
from flask import abort
from flask import request
import jsonpickle

from APIDB.GestorAlumnosSQL import GestorAlumnos

app = Flask(__name__)

############################
#   COLECCIÓN ALUMNOS      #
############################

@app.route('/alumnos',methods=['GET'])
def getAlumnos():
    return jsonpickle.encode(GestorAlumnos.getAlumnos())

@app.route('/alumnos',methods=['PUT'])
def putAlumnos():
    return "puting algo \n"

@app.route('/alumnos',methods=['DELETE'])
def delAlumnos():
    return "deleting algo \n"

@app.route('/alumnos',methods=['POST'])
def postAlumnos():
    '''
    Método que inserta un nuevo alumno en el sistema.
    curl -d "nombre=Juan&dni=45601218Z&direccion=Calle arabl&localidad=Jerez de la frontera&provincia=Granada&fecha_nac=1988-2-6&telefono=677164459" -i -X POST localhost:8080/alumnos
    '''
    if 'dni' in request.form:
        #Presente el DNI al menos podemos grabar el alumno en el sistema.        r
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
#   ENTIDAD ALUMNO  #
#####################

@app.route('/alumnos/<string:id_alumno>',methods=['GET'])
def getAlumno(id_alumno):
    '''
    Devuelve todos los datos de un alumno buscado por su id
    en caso de existir en la base de datos.
    curl -i -X GET localhost:8080/alumnos/11223344A

    '''
    #Si no tiene el número correcto de caracteres el identificador.
    if len(id_alumno) != 9:
        abort(400)

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
    if len(id_alumno) != 9:
        abort(400)

    salida = GestorAlumnos.delAlumno(id_alumno)
    if salida=="Elemento no encontrado":
        abort(404)
    else:
        return 'Elemento eliminado'

@app.route('/alumnos/<string:id_alumno>/profesores',methods=['GET'])
def getProfesores(id_alumno):
    '''
    curl -i -X GET localhost:8080/alumnos/1/profesores
    '''
    return jsonpickle.encode(GestorAlumnos.getProfesores(id_alumno))

@app.route('/alumnos/<string:id_alumno>/asignaturas',methods=['GET'])
def getAsignaturas(id_alumno):
    '''
    curl -i -X GET localhost:8080/alumnos/1/asignaturas
    '''
    return jsonpickle.encode(GestorAlumnos.getAsignaturas(id_alumno))

@app.route('/alumnos/<string:id_alumno>/cursos',methods=['GET'])
def getCursos(id_alumno):
    '''
    curl -i -X GET localhost:8080/alumnos/1/cursos
    '''
    return jsonpickle.encode(GestorAlumnos.getCursos(id_alumno))

if __name__ == '__main__':
    app.run(debug=True)
