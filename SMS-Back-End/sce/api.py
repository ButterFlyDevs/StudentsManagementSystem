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


@app.route('/prueba',methods=['GET']) #tested
def doSomething():
    """
    Función usada como prueba de vida del microservicio
    Prueba del estado de la API.
    curl -i -X GET localhost:8003/prueba
    """
    if v:
        print nombreMicroservicio
        print ' Llamando a /prueba GET doSomething() \n'


    return 'SCE MicroService is RUNING!\n'


@app.route('/resumenesControlesAsistencia', methods=['POST']) #tested
def  obtenerResumenesControlesAsistencia():
    """
    curl -d "idProfesor=22" -i -X POST localhost:8003/resumenesControlesAsistencia
    curl -d "idProfesor=22&idAsignatura=44" -i -X POST localhost:8003/resumenesControlesAsistencia
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
    if v:
        print nombreMicroservicio
        print ' Llamando a /resumenesControlesAsistencia POST resumenesControlesAsistencia() \n'
        print ' Request: '+str(request.form)


    if request.form['idProfesor']:
        print 'YEAH'

    #Usamos .get con el uso de None para que en el caso de no exisitir devuelva None

    if request.form.get('idProfesor', None) is None:
        idProfesor=None
    else:
        idProfesor=int(request.form['idProfesor'])

    if request.form.get('idAsignatura', None) is None:
        idAsignatura=None
    else:
        idAsignatura=int(request.form['idAsignatura'])

    if request.form.get('idClase', None) is None:
        idClase=None
    else:
        idClase=int(request.form['idClase'])

    if request.form.get('fechaHoraInicio', None) is None:
        fechaHoraInicio=None
    else:
        fechaHoraInicio=int(request.form['fechaHoraInicio'])

    if request.form.get('fechaHoraFin', None) is None:
        fechaHoraFin=None
    else:
        fechaHoraFin=int(request.form['fechaHoraFin'])

    return jsonpickle.encode(Gestor.obtenerResumenesControlAsistencia(idProfesor=idProfesor,
                                                                      idAsignatura=idAsignatura,
                                                                      idClase=idClase,
                                                                      fechaHoraInicio=fechaHoraInicio,
                                                                      fechaHoraFin=fechaHoraFin
                                                                      ))

# Métodos sobre Controles De Asistencia
#----------------------------------------------------------------------------------------------------------------#

@app.route('/controlesAsistencia', methods=['POST']) #tested
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
        {"microControlesAsistencia": [
            {
              "asistencia" : 1,
              "retraso": 0,
              "retrasoTiempo" : 0,
              "retrasoJustificado" : 0,
              "uniforme" : 1,
              "idAlumno" : 11
            },
            {
              "asistencia" : 0,
              "retraso": 1,
              "retrasoTiempo" : 1,
              "retrasoJustificado" : 1,
              "uniforme" : 0,
              "idAlumno" : 15
            }
          ],
        "idProfesor" : 22,
        "idClase" : 33,
        "idAsignatura" : 44
       }

    Ejemplo de salida::

        {'status': 'OK', 'key': 22L}
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

    #Devolvemos el mensaje
    return jsonpickle.encode(status)

@app.route('/controlesAsistencia/<int:idControlAsistencia>', methods=['GET']) #tested
def obtenerControlAsistencia(idControlAsistencia):
    """
    Devuelve un control de asitencia completo, es decir, un control realizado por un profesor que
    imparte una asignatura concreta en una clase concreta en una fecha y hora a unos alumnos concretos.

    curl -i -X GET localhost:8003/controlAsistencia/4996180836614144
    """
    #Info de seguimiento
    if v:
        print nombreMicroservicio
        print ' Llamando a /controlAsistencia/'+ str(idControlAsistencia) +' GET obtenerControlAsistencia()'
        print locals()

    #Llamamos al gestor y convertimos su respuesta en un objeto json
    return jsonpickle.encode(Gestor.obtenerControlAsistencia(idControlAsistencia))

@app.route('/controlesAsistencia/<int:idControlAsistencia>', methods=['DELETE']) #tested
def eliminarControlAsistencia(idControlAsistencia):
    """
    Elimina un control de asitencia completo. Ver doc: def eliminarControlAsistencia(...) del gestor.

    curl -i -X DELETE localhost:8003/controlAsistencia/4996180836614144
    """
    #Info de seguimiento
    if v:
        print nombreMicroservicio
        print ' Llamando a /controlAsistencia/'+ str(idControlAsistencia) +' DELTE eliminarControlAsistencia()'
        print locals()

    #Llamamos al gestor y convertimos su respuesta en un objeto json
    return jsonpickle.encode(Gestor.eliminarControlAsistencia(idControlAsistencia))


# Métodos de las entidades de refencia básicas Alumno, Profesor, Clase y Asignatura.
#----------------------------------------------------------------------------------------------------------------#

@app.route('/entidadesReferencia', methods=['POST']) #tested
def insertarEntidad():
    """
    Inserta una entidad de referencia del tipo pasado en el DataStore.

    Método **POST** (los datos pueden pasarse como payload).

    Las entidades de referencia son aquellas que son copia (muy resumida) de las almacenadas en el SBD
    para que cuando se quiera obtener el nombre de una de ellas el SCE no tenga que acceder al SBD, porque tenga una copia el.

    :param tipo: tipo en el que queremos hacer una insercción de una entidad.
    :param idEntidad: id con la que se quiere guardar la entidad en la tabla de su tipo (no es la clave en el datastore).
    :param nombreEntidad: nombre completo de la entidad (ejemplo: En caso de profesor sería su nombre completo).
    :type tipo: string ('Alumno', 'Profesor', 'Clase', 'Asignatura')
    :type idEntidad: int
    :type nombreEntidad: string
    :returns: Mensaje de control
    :rtype: json del diccionario que devuelve el gestor.

    Ejemplo::

          >>> curl -X POST -d "tipo=Alumno&idEntidad=3242&nombreEntidad=alumnoNuevo"  localhost:8003/entidadesReferencia
          {"status": "OK"}
          >>> res = requests.post('localhost:8003/entidadesReferencia', data={ 'tipo': 'Profesor', 'idEntidad': 3135, 'nombreEntidad': 'nombreProfesor' })
          >>> jsonpickle.decode(res.text)
          {"status": "OK"}
    """
    if v:
        print nombreMicroservicio
        print ' Llamando a /entidadesReferencia POST insertarEntidad()'
        print " Request: "
        print request.form


    return jsonpickle.encode(Gestor.insertarEntidad(request.form['tipo'], int(request.form['idEntidad']), request.form['nombreEntidad']))

#PUT is most-often utilized for **update** capabilities
# http://www.restapitutorial.com/lessons/httpmethods.html
@app.route('/entidadesReferencia', methods=['PUT']) #tested
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

#El método DELETE no acepta parámetros pen el body por tanto hay que pasarlos por la url
@app.route('/entidadesReferencia/<string:tipo>/<int:idEntidad>', methods=['DELETE']) #tested
def eliminarEntidad(tipo, idEntidad):
    """
    Elimina una entidad de las de referencia en el DataStore.

    :param tipo: tipo en el que queremos hacer una insercción de una entidad
    :param idEntidad: id con la que se quiere guardar la entidad en la tabla de su tipo (no es la clave en el datastore)
    :type tipo: string ('Alumno', 'Profesor', 'Clase', 'Asignatura')
    :type idEntidad: int
    :returns: Mensaje de control
    :rtype: json del diccionario que devuelve el gestor.

    Ejemplo::

          curl -X DELETE localhost:8003/entidadesReferencia/Alumno/3242

    """

    if v:
        print nombreMicroservicio
        print ' Llamando a /entidadesReferencia DELETE eliminarEntidad()'
        print " Request: "
        print request.form


    return jsonpickle.encode(Gestor.eliminarEntidad(tipo, int(idEntidad)))



if __name__ == '__main__':
    app.run(debug=True)
