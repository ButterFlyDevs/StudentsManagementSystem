# -*- coding: utf-8 -*-
"""
Api Rest del microservicio SCE.

.. note::
    Se trata de una apiRest construida con `Flask <http://flask.pocoo.org/>`_ donde cada función
    está decorada con una ruta de flask que responde a las peticiones http.

"""

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


#Definición del nombre de la aplicación
app = Flask(__name__)

#Activar modo verbose para mensajes por terminal.
v=1
nombreMicroservicio = '\n ## Microservicio SCE ##'

# ===Recurso de prueba el estado del servicio.===

"""
Función usada como prueba de vida del microservicio
"""
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
##   COLECCIÓN Control Asistencia    ##
#######################################

#Maybe deprecated
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
    """
    Inserta un control de asistencia en el sistema. Compuesto por muchos controles a estudiantes para una asignatura en una clase con un
    profesor en una fecha y hora determinadas.


    Debería recibir una lista de controles de asistencia sin fecha ni hora porque se la colocará este microservicio (para evitar múltiples problemas)
    Esta lista de controles se envía en formato JSON

    Prueba del método:
    curl -X POST  -H 'content-type: application/json' -d @ejemploControlAsistencia.json localhost:8003/controlesAsistencia
    El fichero sigue el estandar JSON, ver ejemploControlAsistencia.json. Se pueden validar los ficheros en webs como http://jsonlint.com/.

    Ejemlpo::
        {
        	"microControlesAsistencia": [
            {
          	  "asistencia" : 1,
          	  "retraso": 0,
              "retraso_tiempo" : 0,
              "retraso_justificado" : 0,
              "uniforme" : 1,
              "id_alumno" : 11
          	},
            {
              "asistencia" : 0,
          	  "retraso": 1,
              "retraso_tiempo" : 1,
              "retraso_justificado" : 1,
              "uniforme" : 0,
              "id_alumno" : 15
          	}
          ],
        	"id_profesor" : 22,
        	"id_clase" : 33,
        	"id_asignatura" : 44
        }
    """
    #Extraemos el JSON de la petición.
    json = request.get_json()

    if v:
        print nombreMicroservicio
        print ' Llamando a /controlesAsistencia POST insertaControlAsistencia()'
        print ' '+str(len(json['microControlesAsistencia'])) +' controles recibidos\n'
        print " Controles: "
        print json
        print '\n'


    #Llamamos a la función de NDBlib que inserta el conjunto
    status = Gestor.insertarControlAsistencia(json)

    if v:
        print nombreMicroservicio
        print ' /controlesAsistencia POST insertaControlAsistencia()'
        print ' Return:'+str(status)+'\n'

    #Devolvemos la clave que ha sido introducida
    return str(status)

# ===Obtener controles de Asistenca ===

"""
Devuelve un control de asitencia completo, es decir, un control realizado por un profesor que
imparte una asignatura concreta en una clase concreta en una fecha y hora a unos alumnos concretos.

curl -i -X GET localhost:8003/controlAsistencia/4996180836614144
"""

@app.route('/controlAsistencia/<string:idControlAsistencia>', methods=['GET'])
def getControlAsistencia(idControlAsistencia):

    #Info de seguimiento
    if v:
        print nombreMicroservicio
        print ' Llamando a /controlAsistencia/'+ idControlAsistencia +' GET getControlAsistencia()'
        print locals()

    #Llamamos al gestor y convertimos su respuesta en un objeto json
    return jsonpickle.encode(Gestor.obtenerControlAsistencia(idControlAsistencia))

# === OBtener Resumen controles de Asistencia ===

"""
curl -d "idProfesor=22" -i -X POST localhost:8003/resumenesControlesAsistencia
(Dame todos los controles de asistencia (los resúmenes) realizados por el profesor con idProfesor 4)


Devuelve una lista (puede estar vacía) con todos los controles de asistencia que han realizado según
lo que se esté pididiendo. Si se pasa idProfesor, todos los de ese profesor.
No de vuelve una lista con todos los alumnos y lo que el profesor puso sino un resumen de este control realizado,
así cuando un profesor quiera ver todos los detalles entonces podrá pinchár y se le devolverán todos los datos, pero de
eso se encarga otra función.
Los datos a devolver son:

* key = messages.StringField(1, required=True) Clave del resumen para pedir todas los controles en otro momento.
* fecha = messages.StringField(2)
* idclase = messages.StringField(3)
* nombreClase = messages.StringField(4)
* idasignatura = messages.StringField(5)
* nombreAsignatura = messages.StringField(6)
* idprofesor = messages.StringField(7)
* nombreProfesor = messages.StringField(8)
"""
@app.route('/resumenesControlesAsistencia', methods=['POST'])
def  getResumenesControlesAsistenciaConParametros():

    if v:
        print nombreMicroservicio
        print ' Llamando a /resumenesControlesAsistencia POST resumenesControlesAsistencia() \n'
        print ' Request: '+str(request.form)

    return jsonpickle.encode(Gestor.obtenerResumenesControlAsistencia(idProfesor=request.form['idProfesor']))


@app.route('/entidadesReferencia', methods=['POST'])
def insertarEntidad():
    """
    Inserta una entidad de referencia del tipo pasado en el DataStore.

    Las entidades de referencia son aquellas que son copia (muy resumida) de las almacenadas en el SBD
    para que cuando se quiera obtener el nombre de una de ellas el SCE no tenga que acceder al SBD, porque tenga una copia el.

    :param tipo: tipo en el que queremos hacer una insercción de una entidad
    :param idEntidad: id con la que se quiere guardar la entidad en la tabla de su tipo (no es la clave en el datastore)
    :param nombreEntidad: nombre completo de la entidad
    :type tipo: string ('Alumno', 'Profesor', 'Clase', 'Asignatura')
    :type idEntidad: int
    :type nombreEntidad: string
    :returns: Mensaje de control
    :rtype: json del diccionario que devuelve el gestor.

    Ejemplo::

          curl -X POST -d "tipo=Alumno&idEntidad=3242&nombreEntidad=alumnoNuevo"  localhost:8003/entidadesReferencia

    """
    if v:
        print nombreMicroservicio
        print ' Llamando a /entidadesReferencia POST insertarEntidad()'
        print " Request: "
        print request.form


    return jsonpickle.encode(Gestor.insertarEntidad(request.form['tipo'], int(request.form['idEntidad']), request.form['nombreEntidad']))


#PUT is most-often utilized for **update** capabilities
# http://www.restapitutorial.com/lessons/httpmethods.html
@app.route('/entidadesReferencia', methods=['PUT'])
def modificarEntidad():
    """
    Modifica una entidad de las de referencia en el DataStore.

    Las entidades de referencia son aquellas que son copia (muy resumida) de las almacenadas en el SBD
    para que cuando se quiera obtener el nombre de una de ellas el SCE no tenga que acceder al SBD, porque tenga una copia el.

    :param tipo: tipo en el que queremos hacer una insercción de una entidad
    :param idEntidad: id con la que se quiere guardar la entidad en la tabla de su tipo (no es la clave en el datastore)
    :param nombreEntidad: nombre completo de la entidad
    :type tipo: string ('Alumno', 'Profesor', 'Clase', 'Asignatura')
    :type idEntidad: int
    :type nombreEntidad: string
    :returns: Mensaje de control
    :rtype: json del diccionario que devuelve el gestor.

    Ejemplo::

          curl -X PUT -d "tipo=Alumno&idEntidad=3242&nombreEntidad=alumnoSuperNuevo"  localhost:8003/entidadesReferencia

    """

    if v:
        print nombreMicroservicio
        print ' Llamando a /entidadesReferencia PUT modificarEntidad()'
        print " Request: "
        print request.form


    return jsonpickle.encode(Gestor.modificarEntidad(request.form['tipo'], int(request.form['idEntidad']), request.form['nombreEntidad']))



if __name__ == '__main__':
    app.run(debug=True)
