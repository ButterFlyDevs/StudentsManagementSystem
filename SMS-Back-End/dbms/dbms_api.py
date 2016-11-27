# -*- coding: utf-8 -*-

from flask import Flask, Response
from flask import abort, make_response
from flask import request
import jsonpickle
import logging
from logging.handlers import RotatingFileHandler
from dbapi.entities_manager import EntitiesManager
from dbapi.GestorCredencialesSQL import GestorCredenciales

import datetime

import json
from termcolor import colored


app = Flask(__name__)


#file_handler = logging.FileHandler('app.log', 'rw')
#app.logger.addHandler(file_handler)
#app.logger.setLevel(logging.INFO)


# Activating verbose mode
v = 1

# Activating scms connection.
c = 0

microservice_name = '\n ## dbms Data Base mService ##'


class MyEncoder(json.JSONEncoder):
    """
    Class to provide a personal way to adapt specific objects to json
    when the default isn't enough for us.
    """

    def default(self, obj):
        if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
            # We can select between two formats, is some places people prefer iso.
            #return obj.ctime()  # Example: Sun Oct 16 08:23:29 2016
            return obj.isoformat()  # Example: '2016-10-16T08:23:02

        return json.JSONEncoder.default(self, obj)


def process_response(response):
    """
    Function that process the response of entites manager
    to adjust to APIRest communications, reading the error
    messages and adjust this to the standard REST, and in
    case of error adding this in body of response becasue
    the user maybe want to be informed.

    :param response: a list with three params: status, data and log.
    :return:
    """

    print 'In process response'
    print response

    """
    Function to build a response with sense.
    :param self:
    :param response:
    :return:

    MySQL error standard codes that is processed.
        1452: Cannot add or update a child row: a foreign key constraint fails
        1054 unknown column, is when a value isn't a column in database
        1062: Duplicate entry
        1065: Query was empty
        1146: Table x doesn't exist.
        -1:   When don't exists result, as a in a retrieved "related" data when there aren't related info.

    """

    if response['status'] == 1:
        # return json.dumps(response['data'], cls=MyEncoder)
        #app.logger.info('informing')

        return make_response(Response(json.dumps(response['data'], cls=MyEncoder), mimetype='application/json'))

    elif response['status'] == -1:
        # The element that it searched doesn't exists.
        abort(404)  # Is returned standard "Not found" error.

    elif response['status'] in [1054, 1452, 1146]:
        abort(404, response['log'])  # The same plus log.

    elif response['status'] == 1062:

        # 409 Conflict because the item already exists in database and the user can't create another.
        # resource with the same values.
        abort(409, response['log'])

    else:
        # Another problem that we don't have identified.
        abort(500)

#####################################################
#  Definition of Data Base micro Service REST API   #
#####################################################






# Test method.
@app.route('/test',methods=['GET'])
def test():
    """
    Test resource.

    Example of use:
    curl -i -X GET localhost:8002/test
    """
    return json.dumps({'dbms_api_test_status': 'ok'})


#################################
#   Resources about entities    #
#################################


@app.route('/entities/<string:kind>', methods=['POST'])
def post_entity(kind):
    """
    Insert a entity in the database, with a special input format:

    Input:

        Json payload:
        {
          kind: string, kind of entity that is wanted inserted in the database.
          data: dict, with pairs: key (name of value in database), value (value to save in this key in database)
        }

    Json return:

    Return:
        A json with the entire entity which is saved in database (with all extra control values) or error status code.

    Example of use:
        curl -H "Content-Type: application/json" -X POST -d '{ "data": {"name": "María"} }' localhost:8002/entities/student
        curl -H "Content-Type: application/json" -X POST -d '{"data": {"course": 1, "word": "B", "level": "ESO"} }' localhost:8002/entities/class

    Example of return:
        {"createdBy": 1, "course": 5, "createdAt": "Thu Sep 22 16:09:36 2016", "word": "B", "level": "Primary", "classId": 19}

    If we want to use a file instead of:
        curl -H "Content-Type: application/json" -X POST -d @entityData.json localhost:8002/entidades

    """

    raw_data = request.get_json()

    print colored('mSDBapi.putEntity', 'green')
    print colored(raw_data, 'green')

    data = raw_data.get('data', None)

    if data is None:
        abort(400)

    if data is not None:
        for key, value in data.iteritems():
            if type(value) is not int:
                data[key] = value.encode('utf-8')

    # When are really saved data in database
    response = EntitiesManager.put(kind, data)

    """
    if c:
        salida = salidaGestor
        print colored(salidaGestor, 'green')

        #Si la salida del gestor es correcta llamaremos al mSCE para añadir un elemento de referencia:
        if salidaGestor['status'] == 'OK':
            print colored('Entidad creada con Exito en SBD, enviando datos al SCE', 'red')
            url = "http://%s/" % modules.get_hostname(module="sce")
            url+="entidadesReferencia"

            #Creamos un diccionario con los datos.
            dicDatos = {
              'tipo' : tipo,
              #Usamos el id de la entidad que nos devuelve el gestor.
              'idEntidad': salidaGestor['idEntidad'],
            }

            #Dependiendo del tipo de entidad que recibamos componemos el nombre de la entidad de una manera u otra
            if tipo == 'Alumno' or tipo == 'Profesor':
                dicDatos['nombreEntidad'] = datos['nombre']+' '+datos['apellidos']

            if tipo == 'Clase':
                dicDatos['nombreEntidad'] = str(datos['curso'])+' '+str(datos['grupo'])+' '+datos['nivel']

            if tipo == 'Asignatura':
                dicDatos['nombreEntidad'] = datos['nombre']


            print colored(dicDatos, 'green')

            print colored(url,'green')
            req = urllib2.Request(url, json.dumps(dicDatos), {'Content-Type': 'application/json'})
            print colored(req, 'green')
            f = urllib2.urlopen(req)
            response = json.loads(f.read())
            print colored(response, 'green')
            f.close()

            if response['status'] != 'OK':
                salida['status'] = 'FAIL'
                salida['info'] = 'SCE subcall fail'

            print colored(response, 'green')


        #En caso de que la entidad introducida sea un profesor se cargarán lascredenciales por defecto en el sistema.
        if tipo == 'Profesor':
            print ' Profesor creado con éxito. Creando sus credenciales de acceso al sistema.'
            #Creamos las credenciales del usuario en la tabla credenciales usando el id del usuario que devuelve nuevoProfesor
            #Por defecto el alias y el password de un profesor en el sistemas serán su dni
            #salida Creacion CredencialespostProfesor
            salidaCC=GestorCredenciales.postCredenciales(salidaGestor['idEntidad'], dicDatos['nombreEntidad'], datos['dni'], datos['dni'], 'admin')
            if salidaCC != 'OK':
                salida['status'] = 'FAIL'
                salida['info']='SBD credential creation fail'


        ######


        #Realizamos la petición al gestor y devolvemos la respuesta transformada a json.
        #return json.dumps(salidaGestor)
        print colored(salida, 'green')
        return json.dumps(salida)
    """

    return process_response(response)


@app.route('/entities/<string:kind>', methods=['GET']) #Si pedimos todas las entidades de un tipo
@app.route('/entities/<string:kind>/<int:entity_id>', methods=['GET']) #Si pedimos una entidad concreta de un tipo
def get_entities(kind, entity_id=None):
    """
    Retrieve info about entities, a list of all of them with all info or specific params or all data from one.

    Example of use:

    curl  -i -X GET localhost:8002/entities/student  -> All items of student list with all data
    curl  -i -X GET localhost:8002/entities/student?params=name  -> Only params sent from all students
    curl  -i -X GET  localhost:8002/entities/student/1  -> All data from student with id = 1
    """
    return process_response(EntitiesManager.get(kind, entity_id, request.args.get('params', None)))


@app.route('/entities/<string:kind>/<int:entity_id>', methods=['PUT'])
def put_entities(kind, entity_id):  # UPDATE
    """
    curl -H "Content-Type: application/json" -X PUT -d '{ "name": "NombreModificado" }' localhost:8002/entities/teacher/1
    """

    raw_data = request.get_json()

    print colored('dbms.apigms_api.update_entities', 'green')
    print colored(request.headers, 'green')

    app.logger.info('hi')

    print colored(raw_data, 'red')

    #data = raw_data.get('data', None)

    if raw_data is None:
        abort(400)

    if raw_data is not None:
        for key, value in raw_data.iteritems():
            if type(value) is not int:
                raw_data[key] = value.encode('utf-8')

    return process_response(EntitiesManager.update(kind, entity_id, raw_data))



@app.route('/entities/<string:kind>/<int:entity_id>', methods=['DELETE'])
def delete_entity(kind, entity_id):
    """
    curl  -i -X  DELETE localhost:8002/entities/subject/1
    """
    return process_response(EntitiesManager.delete(kind, entity_id))


@app.route('/entities/<string:kind>/<int:entity_id>/<string:related_kind>', methods=['GET'])
def get_related_entities(kind, entity_id, related_kind):
    """
    curl -i -X GET localhost:8002/entities/student/1/teacher

    curl -X GET localhost:8002/entities/teacher/4/imparts | python -mjson.tool

    """
    return process_response(EntitiesManager.get_related(kind, entity_id, related_kind))


##########################
# COLECCIÓN CREDENCIALES #
##########################

@app.route('/credenciales', methods=['GET'])
def getCredenciales():
    '''
    Devuelve las credenciales de todos los usuarios almacenadas en la base de datos.
    curl -i -X GET localhost:8002/credenciales
    '''
    return jsonpickle.encode(GestorCredenciales.getCredenciales())

@app.route('/credenciales', methods=['POST'])
def postCredenciales():
    '''
    Introduce las credenciales de un usuario en el sistema.
    curl -d "idUsuario=1&nombre=lucas&username=juan&password=677164459&rol=admin" -i -X POST localhost:8002/credenciales
    '''
    #Devolvemos directamente la salida de la función.
    return GestorCredenciales.postCredenciales(request.form['idUsuario'], request.form['nombre'], request.form['username'], request.form['password'], request.form['rol'] )

@app.route('/comprobarAccesoUsuario', methods=['POST'])
def comprobarAccesoUsuario():
    '''
    Comprueba que el login y el password de un usuario le da acceso al sistema.
    curl -d "username=46666&password=46666" -i -X POST localhost:8002/comprobarAccesoUsuario
    '''

    #Info de seguimiento
    if v:
        print nombreMicroservicio
        print ' Recurso: /comprobarAccesoUsuario , metodo: POST'
        print " Petición: "
        print ' '+str(request.form)

    salida=GestorCredenciales.comprobarUsuario(request.form['username'], request.form['password'])

    #Info de seguimiento
    if v:
        print nombreMicroservicio
        print salida
        print ' Return /comprobarAccesoUsuario: '+str(salida)+'\n'

    #Devolvemos los datos en formato JSON
    return jsonpickle.encode(salida)

if __name__ == '__main__':
    handler = RotatingFileHandler('dbms_api_log.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True)

