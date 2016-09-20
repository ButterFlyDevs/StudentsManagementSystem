# -*- coding: utf-8 -*-

from flask import Flask, request
from flask import abort
from flask import request
import jsonpickle

from APIDB.GestorEntidades import GestorEntidades
from APIDB.GestorCredencialesSQL import GestorCredenciales

from google.appengine.api import modules
from google.appengine.api import urlfetch
import urllib
import urllib2
import json
from termcolor import colored

app = Flask(__name__)

#Activar modo verbose
v=1
nombreMicroservicio = '\n ## Microservicio BD ##'

#####################################################
## DEFINICIÓN DE LA API REST del MICROSERVICIO SBD ##
#####################################################

@app.route('/test',methods=['GET'])
def test():
    """
    Devuelve una lista de todos los estudiantes.
    curl -i -X GET localhost:8002/test
    """
    return 'OK'

############################
#   COLECCIÓN ENTIDADES    #
############################

@app.route('/entidades', methods=['POST'])
def putEntidad():
    """
    Inserta una entidad en el sistema, debido a que puede introducir cualquier tipo de entidad, se acepta la siguient lista
    de parámetros:

    parámetros: json con los datos:
        tipo: string con el tipo de entidad que se quiere introducir en el sistema.
        datos: json con todos los parámetros

    devuelve: un json con el estado, con el formato:
    {
        'status': '<estado de la ejecución (OK, FAIL)>',
        'info': '<información extra en caso de ser necesaria',
        'mySqlCode': '<codigo de estado de mysql, en caso de que se tenga.'
        'idEntidad': '<id de la entidad en caso de ser creada>'
    }

    Ejemplo de uso:
    curl -H "Content-Type: application/json" -X POST -d '{"tipo": "Alumno", "datos": {"nombre": "María"} }' localhost:8002/entidades
    #En caso de usar un fichero
    curl -H "Content-Type: application/json" -X POST -d @datosEntidad.json localhost:8002/entidades

    """

    #Definimos un diccionario para la salida, puede contener info la creación de la entidad, de las credenciales en caso de ser
    #un profesor y de la creación de la entidad de referencia en el mSCE.
    salida = {}

    #Extraemos el json de la petición
    data = request.get_json()

    #Extraemos los datos de la entidad y pasamos todos los elementos a utf-8
    datos = data.get('datos', None)
    if datos != None:
        for key, value in datos.iteritems():
            print type(value)
            if type(value) is not int:
                datos[key] = value.encode('utf-8')

    tipo = data.get('tipo', None)


    #Llamamos a la librería para guarar los datos y recuperamos la respuesta.
    salidaGestor = GestorEntidades.putEntidad(tipo=tipo, datos=datos)

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

@app.route('/entidades/<string:tipo>', methods=['GET']) #Si pedimos todas las entidades de un tipo
@app.route('/entidades/<string:tipo>/<int:idEntidad>', methods=['GET']) #Si pedimos una entidad concreta de un tipo
def getEntidades(tipo, idEntidad=None):
    """
    curl -i -X GET localhost:8002/entidades/prueba

    curl  -i -X GET localhost:8002/entidades/Alumno
    curl  -i -X GET  localhost:8002/entidades/Alumno/1
    geting
    """

    if idEntidad != None: #Nos piden todos los datos de una entidad concreta de un tipo concreto.
        #Devolvemos los datos en json (transformando el diccionario que nos devuelve el gestor)
        return json.dumps(GestorEntidades.getEntidades(tipo=str(tipo), idEntidad=str(idEntidad)))
    else: #Nos piden todas las entidades de un tipo (info resumida)
        return json.dumps(GestorEntidades.getEntidades(tipo=str(tipo)))
        #return GestorEntidades.getEntidades(tipo=request.args['tipo'], idEntidad=request.args['idEntidad'])

@app.route('/entidades', methods=['PUT'])
def modEndidad():
    """
    curl -H "Content-Type: application/json" -X PUT -d '{"tipo": "Alumno", "idEntidad": "1", "campoACambiar": "nombre", "nuevoValor": "Lucía" }' localhost:8002/entidades
    """
    data = request.get_json()
    print colored(data, 'red')


    #HERe
    #Tras esto deberíamos llamar al servicio de SCE para enviar los datos simples al SCE para actualizar las entidades
    ###
    ### Cuando se modifica el nombre o la imagen de una entidada alumno hay que llamar al servicio SCE para que actualice
    ### los datos rápidos en la NDB para que los controles de asistencia tengan los datos actualizados.


    return json.dumps(GestorEntidades.modEntidad(tipo=data.get('tipo', None), idEntidad=data.get('idEntidad', None), campoACambiar=data.get('campoACambiar', None), nuevoValor=data.get('nuevoValor', None)))

@app.route('/entidades/<string:tipo>/<int:idEntidad>', methods=['DELETE'])
def delEntidad(tipo, idEntidad):
    """
    curl  -i -X  DELETE localhost:8002/entidades/Alumno/1
    """
    return json.dumps(GestorEntidades.delEntidad(tipo=str(tipo), idEntidad=str(idEntidad)))

@app.route('/entidades/<string:tipoBase>/<int:idEntidad>/<string:tipoBusqueda>', methods=['GET'])
def getEntidadesRelacionadas(tipoBase, idEntidad, tipoBusqueda):
    """
    curl -i -X GET localhost:8002/entidades/Alumno/1/Profesor
    """
    return json.dumps(GestorEntidades.getEntidadesRelacionadas(tipoBase=str(tipoBase), idEntidad=str(idEntidad), tipoBusqueda=str(tipoBusqueda)))

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
    app.run(debug=True)
