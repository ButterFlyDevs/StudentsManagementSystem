# -*- coding: utf-8 -*-

######################################################
## DEFINICIÓN DE LA API REST del MICROSERVICIO SCE  ##
######################################################

from flask import Flask
from flask import abort
from flask import request
import jsonpickle
import Estructuras
import datetime
from NDBlib.gestor import Gestor



#from NDBlib import EstrutcutrasNDB.ControlAsistencia


#Definición del nombre de la aplicación
app = Flask(__name__)

#Activar modo verbose para mensajes por terminal.
v=1
nombreMicroservicio = '\n ## Microservicio SCE ##'

#Recurso de prueba el estado del servicio.
@app.route('/prueba',methods=['GET'])
def doSomething():
    '''
    Prueba del estado de la API.
    curl -i -X GET localhost:8003/prueba
    '''
    if v:
        print nombreMicroservicio
        print ' Llamando a /prueba GET doSomething() \n'


    return 'SCE MicroService is RUNING!\n'

#######################################
#   COLECCIÓN Control Asistencia      #
#######################################

#Maybe be deprecated
@app.route('/controlesAsistencia', methods=['GET'])
def  getAllControlesAsistencia():
    '''
    Devuelve todos los controles de asistencia.
    curl -i -X GET localhost:8003/controlesAsistencia
    '''

    if v:
        print nombreMicroservicio
        print 'Llamando a /controlesAsistencia GET getAllControlesAsistencia()'

    listaCAs=Gestor.obtenerALLCA()
    '''
    for a in listaCAs:
        print a.asistencia
        json = jsonpickle.encode(a)
        print jsonpickle.decode(json)
    '''


    if v:
        print nombreMicroservicio
        print ' Llamando a /controlesAsistencia GET getAllControlesAsistencia()'
        print ' Salida: '
        print str(listaCAs)

    return jsonpickle.encode(listaCAs)


@app.route('/controlesAsistencia', methods=['POST'])
def  insertaControlAsistencia():
    '''
    Inserta un control de asistencia en el sistema. Compuesto por muchos controles a estudiantes para una asignatura en una clase con un
    profesor en una fecha y hora determinadas.


    Debería recibir una lista de controles de asistencia sin fecha ni hora porque se la colocará este microservicio (para evitar múltiples problemas)
    Esta lista de controles se envía en formato JSON

    Prueba del método:
    curl -X POST  -H 'content-type: application/json' -d @pruebaJson.json localhost:8003/controlesAsistencia
    El fichero sigue el estandar JSON, ver pruebaJson.json. Se pueden validar los ficheros en webs como http://jsonlint.com/.

    '''

    #Extraemos el JSON de la petición.
    json = request.get_json()

    if v:
        print nombreMicroservicio
        print ' Llamando a /controlesAsistencia POST insertaControlAsistencia()'
        print str(len(json['controles'])) +' controles recibidos\n'
        print " Controles: "
        print json


    #Llamamos a la función de NDBlib que inserta el conjunto
    status = Gestor.insertarConjuntoControlAsistencia(json['controles'])



    '''

    #Dividimos la fecha en partes usando el separador -
    fecha = request.form['fecha'].split('-')

    print fecha

    #Creamos un objeto datetime con estas divisiones, siguiendo el formato de datetime:

    #Ejemplo: 05/10/09 18:00 ; date = datetime.datetime(2009, 10, 5, 18, 00)
    #                 año        mes      día       hora     minutos
    date = datetime.datetime(int(fecha[2]), int(fecha[1]), int(fecha[0]), int(fecha[3]), int(fecha[4]))

    #Usando el gestor insertamos el objeto en la base de datos, ajustando los datos que nos llegan a los tipos que se esperan.
    clave=Gestor.insertarControlAsistencia(
                                        date,
                                        parseBoolean(request.form['asistencia']),
                                        parseBoolean(request.form['uniforme']),
                                        parseBoolean(request.form['retraso']),
                                        int(request.form['retraso_tiempo']),
                                        parseBoolean(request.form['retraso_justificado']),
                                        int(request.form['id_alumno']),
                                        int(request.form['id_profesor']),
                                        int(request.form['id_clase']),
                                        int(request.form['id_asignatura']),
                                        )
    '''


    if v:
        print nombreMicroservicio
        print ' /controlesAsistencia POST insertaControlAsistencia()'
        print ' Return:'+str(status)+'\n'

    #Devolvemos la clave que ha sido introducida
    return str(status)


@app.route('/controlAsistencia/<string:idControlAsistencia>', methods=['GET'])
def getControlAsistencia(idControlAsistencia):
    '''
    Devuelve un control de asitencia completo, es decir, un control realizado por un profesor que
    imparte una asignatura concreta en una clase concreta en una fecha y hora a unos alumnos concretos.

    curl -i -X GET localhost:8003/controlAsistencia/4644337115725824
    '''

    #Info de seguimiento
    if v:
        print nombreMicroservicio
        print ' Llamando a /controlAsistencia/'+ idControlAsistencia +' GET getControlAsistencia()'
        print locals()

    #Llamamos al gestor y convertimos su respuesta en un objeto json
    return jsonpickle.encode(Gestor.obtenerControlAsistencia(idControlAsistencia))




###############################################
#   COLECCIÓN Resumen Control Asistencia      #
###############################################

@app.route('/resumenesControlesAsistenciaEspecificos', methods=['POST'])
def  getResumenesControlesAsistenciaConParametros():

    '''

    curl -d "idProfesor=3" -i -X POST localhost:8003/resumenesControlesAsistenciaEspecificos
    (Dame todos los controles de asistencia (los resúmenes) realizados por el profesor con idProfesor 4)


    Devuelve una lista (puede estar vacía) con todos los controles de asistencia que han realizado según
    lo que se esté pididiendo. Si se pasa idProfesor, todos los de ese profesor.
    No de vuelve una lista con todos los alumnos y lo que el profesor puso sino un resumen de este control realizado,
    así cuando un profesor quiera ver todos los detalles entonces podrá pinchár y se le devolverán todos los datos, pero de
    eso se encarga otra función.
    Los datos a devolver son:

        key = messages.StringField(1, required=True) Clave del resumen para pedir todas los controles en otro momento.
        fecha = messages.StringField(2)
        idclase = messages.StringField(3)
        nombreClase = messages.StringField(4)
        idasignatura = messages.StringField(5)
        nombreAsignatura = messages.StringField(6)
        idprofesor = messages.StringField(7)
        nombreProfesor = messages.StringField(8)

    '''
    if v:
        print nombreMicroservicio
        print ' Llamando a /resumenesControlesAsistencia POST resumenesControlesAsistencia() \n'
        print ' Request: '+str(request.form)

    return jsonpickle.encode(Gestor.obtenerResumenesControlAsistencia(idProfesor=request.form['idProfesor']))

############################################################
#   COLECCIÓNES AUXILIARES relacionadas de referencia      #
############################################################

@app.route('/alumnos', methods=['POST'])
def insetarAlumno():
    '''
    curl -X POST -d "idAlumno=1&nombreAlumno=Fernando"  localhost:8003/alumnos
    '''
    if v:
        print nombreMicroservicio
        print ' Llamando a /alumnos POST insertarAlumno()'
        print " Request: "
        print request.form


    return jsonpickle.encode(Gestor.insertarAlumno(request.form['idAlumno'], request.form['nombreAlumno']))
    

@app.route('/asignaturas', methods=['POST'])
def insetarAsignatura():
    '''
    curl -X POST -d "idAsignatura=1&nombreAsignatura=Frances"  localhost:8003/asignaturas
    '''
    if v:
        print nombreMicroservicio
        print ' Llamando a /asignatura POST insertaAsignatura()'
        print " Request: "
        print request.form


    return jsonpickle.encode(Gestor.insertarAsignatura(request.form['idAsignatura'], request.form['nombreAsignatura']))

@app.route('/clases', methods=['POST'])
def insetarClase():
    '''
    curl -X POST -d "idClase=1&nombreClase=1AESO"  localhost:8003/clases
    '''
    if v:
        print nombreMicroservicio
        print ' Llamando a /clase POST insertarClase()'
        print " Request: "
        print request.form


    return jsonpickle.encode(Gestor.insertarClase(request.form['idClase'], request.form['nombreClase']))

@app.route('/profesores', methods=['POST'])
def insertarProfesor():
    '''
    curl -X POST -d "idProfesor=4&nombreProfesor=Eduardo Ros"  localhost:8003/profesores
    '''
    if v:
        print nombreMicroservicio
        print ' Llamando a /profesor POST insertarProfesor()'
        print " Request: "
        print request.form

    return jsonpickle.encode(Gestor.insertarProfesor(request.form['idProfesor'], request.form['nombreProfesor']))

if __name__ == '__main__':
    app.run(debug=True)
