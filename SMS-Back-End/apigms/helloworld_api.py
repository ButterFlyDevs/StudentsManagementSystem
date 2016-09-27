# -*- coding: utf-8 -*-
"""

Hello World API implemented using Google Cloud Endpoints.


"""


import endpoints
#https://cloud.google.com/appengine/docs/python/tools/protorpc/messages/messageclass
from protorpc import messages
from protorpc import message_types
from protorpc import remote
import os

#Doc de urlfetch: https://cloud.google.com/appengine/docs/python/refdocs/google.appengine.api.urlfetch
#Librerías usadas para la llamada a las APIRest de los microservicios
from google.appengine.api import urlfetch
import urllib

#Para el descubrimiento de los módulos
import urllib2
from google.appengine.api import modules
#Para la decodificaciónd e los datos recibidos en JSON desde las APIs
import jsonpickle


from termcolor import colored

import requests

import json

from manejadorImagenes import ManejadorImagenes

#Variable habilitadora del modo verbose
v=True

nombreMicroservicio = '\n ## API Gateway ##'

#Variable del nombre del microservicio de base de datos SBD
sbd="sbd"


# TODO: Replace the following lines with client IDs obtained from the APIs
# Console or Cloud Console.
WEB_CLIENT_ID = 'replace this with your web client application ID'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID


package = 'Hello'
# Función que recibe una cadena como parámetro y la formatea para resolver el problema de los acentos.
def formatText(cadena):
    return cadena.encode('utf-8').decode('utf-8')

def formatTextInput(cadena):
    return cadena.encode('utf-8')


import  mensajes.mensajesSCE as mensajesSCE
import mensajes.otrosMensajes as mensajesSBD


module = modules.get_current_module_name()
instance = modules.get_current_instance_id()

#Decorador que establace nombre y versión de la api
@endpoints.api(name='helloworld', version='v1')
class HelloWorldApi(remote.Service):
    """Helloworld API v1.
    faslkfjñalksf
    laksfjlka
    laksjklj"""


    @endpoints.method(message_types.VoidMessage, mensajesSBD.MensajeRespuesta, path='holaMundo', http_method='GET', name='holaMundo')
    def pruebaHolaMundo(self, request):
        """
        Función de prueba de exposición.
        curl -X GET localhost:8001/_ah/api/helloworld/v1/prueba22
        """
        return mensajesSBD.MensajeRespuesta(message='Hola mundo! \n')

    ##################################################################
    ###   métodos microServicio Base de Datos       mSBD           ###
    ##################################################################

    ###   métodos de ENTIDADES       mSBD     ###

    @endpoints.method( mensajesSBD.Entidad,  mensajesSBD.StatusID, path='entidades', http_method='POST', name='entidades.insertarEntidad')
    def insertarEntidad(self, request):
        """
        Inserta una nueva entidad en la base de datos del sistema, a través del SBD.

        curl -i -d "tipo=CienciasExperimentales" -X POST -G localhost:8001/_ah/api/helloworld/v1/entidades
        curl -H "Content-Type: application/json" -X POST -d '{"tipo": "Alumno", "datos": {"nombre": "María"} }'  localhost:8001/_ah/api/helloworld/v1/entidades
        curl -H "Content-Type: application/json" -X POST -d '{"tipo": "Alumno", "datos": {"nombre": "María", "apellidos": "Luzán"} }'  localhost:8001/_ah/api/helloworld/v1/entidades
        """


        #Future: debería comprobar el nombre de los parámetros y si alguno está mal escrito devolver un mensaje de fallo
        #y algún tipo de mensaje donde explique esto.

        if v:
            print nombreMicroservicio
            print "Petición POST a entidades.insertarEntidad"
            print "request: "+str(request)
            print '\n'


        tipo = request.tipo
        datos = {}

        if request.datos.nombre != None:
            datos['nombre'] = request.datos.nombre
        if request.datos.apellidos != None:
            datos['apellidos'] = request.datos.apellidos
        if request.datos.dni != None:
            datos['dni'] = request.datos.dni
        if request.datos.direccion != None:
            datos['direccion'] = request.datos.direccion
        if request.datos.localidad != None:
            datos['localidad'] = request.datos.localidad
        if request.datos.provincia != None:
            datos['provincia'] = request.datos.provincia
        if request.datos.fechaNacimiento != None:
            datos['fechaNacimiento'] = request.datos.fechaNacimiento
        if request.datos.telefono != None:
            datos['telefono'] = request.datos.telefono

        if request.datos.curso != None:
            datos['curso'] = request.datos.curso
        if request.datos.grupo != None:
            datos['grupo'] = request.datos.grupo
        if request.datos.nivel != None:
            datos['nivel'] = request.datos.nivel

        if request.datos.idClase != None:
            datos['idClase'] = request.datos.idClase
        if request.datos.idAsignatura != None:
            datos['idAsignatura'] = request.datos.idAsignatura
        if request.datos.idAsociacion != None:
            datos['idAsociacion'] = request.datos.idAsociacion
        if request.datos.idAlumno != None:
            datos['idAlumno'] = request.datos.idAlumno
        if request.datos.idProfesor != None:
            datos['idProfesor'] = request.datos.idProfesor



        #Le decimos al microservicio que queremos conectarnos (solo usando el nombre del mismo), GAE descubre su URL solo.
        url = "http://%s/" % modules.get_hostname(module=sbd)
        url+='entidades'
        req = urllib2.Request(url, json.dumps({'tipo': tipo, 'datos': datos}), {'Content-Type': 'application/json'})
        f = urllib2.urlopen(req)
        response = json.loads(f.read())
        f.close()


        print colored(response, 'green')

        idEntidad=response.get('idEntidad', None)


        idEntidad=response.get('idEntidad', None)
        print idEntidad
        #Si se ha realizado una insercción donde algún microservicio devuelva idEntidad esta se devuelve.
        if idEntidad != None:
            return mensajesSBD.StatusID(status=response['status'], idEntidad=int(idEntidad))
        else:
            return mensajesSBD.StatusID(status=response['status'])

    #Por no haber forma de hacer que funcionen las rutas .../Alumno para la lista completa y ../Alumno/2 para los datos del
    #alumno con id 2 se hacen dos métodos separados.
    @endpoints.method( mensajesSBD.ID_RESOURCE,  mensajesSBD.ListaEntidades ,http_method='GET',path='entidades/{tipo}',name='entidades.getEntidades')
    def getEntidades(self, request):

        """
        curl  localhost:8001/_ah/api/helloworld/v1/entidades/Alumno
        """


        print colored(request.tipo, 'red')
        print colored(request.idEntidad, 'red')
        if not request.idEntidad:
            print 'HELLO'

        url = "http://%s/" % modules.get_hostname(module=sbd)
        url += 'entidades' + '/' + str(request.tipo)
        if request.idEntidad:
            url += '/' + str(request.idEntidad)


        print colored(url, 'green')

        req = urllib2.Request(url)
        f = urllib2.urlopen(req)
        response = json.loads(f.read())
        f.close()

        if type(response) is not list:
            message = 'No existe entidad del tipo %s.' % request.tipo
            raise endpoints.NotFoundException(message)


        print colored(response, 'red')

        lista = []

        """
        Como la entidad puede ser de muchos tipos, se analizan todos los campos posibles y se construye
        el mensaje de salida conforme a este, así simplificamos el proceso. En todos los casos habrá keys
        que no estarán en el diccionario que nos devuelve el microservicio, esto no es un problema ya que
        se pondrá None (usando get) y no se enviarán por el mensaje, devolviendo así solo la información que
        el sistema tiene.
        """
        for ent in response:
            entidad = mensajesSBD.DatosEntidadGenerica()
            entidad.nombre = ent.get('nombre', None)
            entidad.apellidos = ent.get('apellidos', None)
            entidad.dni = ent.get('dni', None)
            entidad.direccion = ent.get('direccion', None)
            entidad.localidad = ent.get('localidad', None)
            entidad.provincia = ent.get('provincia', None)
            entidad.fechaNacimiento = ent.get('fechaNacimiento', None)
            entidad.telefono = ent.get('telefono', None)
            entidad.imagen = ent.get('urlImagen', None)
            entidad.curso = ent.get('curso', None)
            entidad.grupo = ent.get('grupo', None)
            entidad.nivel = ent.get('nivel', None)

            lista.append(entidad)
        return mensajesSBD.ListaEntidades(entidades=lista)

    @endpoints.method( mensajesSBD.ID_RESOURCE,  mensajesSBD.DatosEntidadGenerica ,http_method='GET',path='entidades/{tipo}/{idEntidad}',name='entidades.getEntidad')
    def getEntidad(self, request):
        """
        curl  localhost:8001/_ah/api/helloworld/v1/entidades/Alumno/1
        {
         "nombre": "nombrePrueba"
        }
        """

        url = "http://%s/" % modules.get_hostname(module=sbd)
        url += 'entidades' + '/' + str(request.tipo)
        if request.idEntidad:
            url += '/' + str(request.idEntidad)

        req = urllib2.Request(url)
        f = urllib2.urlopen(req)
        response = json.loads(f.read())
        f.close()


        #Si la respuesta del microservicio es nevativa por no haber encontrado el recurso que se le pide,
        #devolvemos el mensaje estandar NotFoundException code 404
        if response == 'Elemento no encontrado':
            message = 'No existe entidad con id %s para el tipo %s.' % (request.idEntidad, request.tipo)
            raise endpoints.NotFoundException(message)

        """
        Como la entidad puede ser de muchos tipos, se analizan todos los campos posibles y se construye
        el mensaje de salida conforme a este, así simplificamos el proceso. En todos los casos habrá keys
        que no estarán en el diccionario que nos devuelve el microservicio, esto no es un problema ya que
        se pondrá None (usando get) y no se enviarán por el mensaje, devolviendo así solo la información que
        el sistema tiene.
        """
        if request.idEntidad:
            entidad = mensajesSBD.DatosEntidadGenerica()
            entidad.nombre = response.get('nombre', None)
            entidad.apellidos = response.get('apellidos', None)
            entidad.dni = response.get('dni', None)
            entidad.direccion = response.get('direccion', None)
            entidad.localidad = response.get('localidad', None)
            entidad.provincia = response.get('provincia', None)
            entidad.fechaNacimiento = response.get('fechaNacimiento', None)
            entidad.telefono = response.get('telefono', None)
            entidad.imagen = response.get('urlImagen', None)
            entidad.curso = response.get('curso', None)
            entidad.grupo = response.get('grupo', None)
            entidad.nivel = response.get('nivel', None)


        return entidad

    @endpoints.method( mensajesSBD.MensajeModificacionEntidad,  mensajesSBD.StatusID, path='entidades', http_method='PUT', name='entidades.modificarEntidad')
    def modEntidad(self, request):
        """
        curl -H "Content-Type: application/json" -X PUT -d '{"tipo": "Alumno", "idEntidad": 1, "campoACambiar": "nombre", "nuevoValor": "Lucía" }'  localhost:8001/_ah/api/helloworld/v1/entidades
        curl -H "Content-Type: application/json" -X PUT -d '{"tipo": "Alumno", "idEntidad": 1, "campoACambiar": "dni", "nuevoValor": "16271625" }'  localhost:8001/_ah/api/helloworld/v1/entidades
        """

        #Le decimos al microservicio que queremos conectarnos (solo usando el nombre del mismo), GAE descubre su URL solo.
        url = "http://%s/" % modules.get_hostname(module=sbd)
        url+='entidades'

        #Codificamos los datos.
        dic = {'tipo': request.tipo,
               'idEntidad': request.idEntidad,
               'campoACambiar': request.campoACambiar,
               'nuevoValor': request.nuevoValor }

        #Realizamos la petición al servicio con los datos codificados al microservicio apropiado.
        result = urlfetch.fetch(url=url, payload=json.dumps(dic), method=urlfetch.PUT, headers={'Content-Type': 'application/json'})
        result = json.loads(result.content)


        return mensajesSBD.StatusID(status=result['status'])

    @endpoints.method( mensajesSBD.ID_RESOURCE,  mensajesSBD.StatusID ,http_method='DELETE',path='entidades/{tipo}/{idEntidad}',name='entidades.delEntidad')
    def delEntidad(self, request):
        """
        curl -X DELETE -G localhost:8001/_ah/api/helloworld/v1/entidades/Alumno/1
        """

        if v:
            print nombreMicroservicio
            print "Petición DELETE a entidades.delEntidad"
            print "request: "+str(request)
            print '\n'

        #Le decimos al microservicio que queremos conectarnos (solo usando el nombre del mismo), GAE descubre su URL solo.
        url = "http://%s/" % modules.get_hostname(module=sbd)
        url += 'entidades' + '/' + str(request.tipo) + '/' + str(request.idEntidad)

        #Usamos el método DELETE con la url
        result = urlfetch.fetch(url=url, method=urlfetch.DELETE)
        result = json.loads(result.content)

        return mensajesSBD.StatusID(status=result['status'])

    @endpoints.method( mensajesSBD.Recursosv2,  mensajesSBD.ListaEntidades, http_method='GET', path='entidades/{tipoBase}/{idEntidad}/{tipoBusqueda}', name='entidades.getEntidadesRelacionadas')
    def getEntidadesRelacionadas(self, request):
        """
        curl -X GET -G localhost:8001/_ah/api/helloworld/v1/entidades/{tipoBase}/{idEntidad}/{tipoBusqueda}
        curl -X GET -G localhost:8001/_ah/api/helloworld/v1/entidades/Alumno/1/Profesor
        """

        if v:
            print nombreMicroservicio
            print "Petición DELETE a entidades.delEntidad"
            print "request: "+str(request)
            print '\n'

        url = "http://%s/" % modules.get_hostname(module=sbd)
        url += 'entidades' + '/' + str(request.tipoBase) + '/' + str(request.idEntidad) + '/' + str(request.tipoBusqueda)

        #Usamos el método DELETE con la url
        result = urlfetch.fetch(url=url, method=urlfetch.GET)
        result = json.loads(result.content)
        print result

        lista = []

        """
        Como la entidad puede ser de muchos tipos, se analizan todos los campos posibles y se construye
        el mensaje de salida conforme a este, así simplificamos el proceso. En todos los casos habrá keys
        que no estarán en el diccionario que nos devuelve el microservicio, esto no es un problema ya que
        se pondrá None (usando get) y no se enviarán por el mensaje, devolviendo así solo la información que
        el sistema tiene.
        """
        for ent in result:
            entidad = mensajesSBD.DatosEntidadGenerica()
            entidad.nombre = ent.get('nombre', None)
            entidad.apellidos = ent.get('apellidos', None)
            entidad.dni = ent.get('dni', None)
            entidad.direccion = ent.get('direccion', None)
            entidad.localidad = ent.get('localidad', None)
            entidad.provincia = ent.get('provincia', None)
            entidad.fechaNacimiento = ent.get('fechaNacimiento', None)
            entidad.telefono = ent.get('telefono', None)
            entidad.imagen = ent.get('urlImagen', None)
            entidad.curso = ent.get('curso', None)
            entidad.grupo = ent.get('grupo', None)
            entidad.nivel = ent.get('nivel', None)

            lista.append(entidad)
        return mensajesSBD.ListaEntidades(entidades=lista)

    @endpoints.method(mensajesSBD.AlumnoCompletoConImagen,  mensajesSBD.StatusID, path='alumnos/insertarAlumno2', http_method='POST', name='alumnos.insertarAlumno2')
    def insertar_alumno2(self, request):


        #Pero antes ponemos el nombre de forma correcta, usando el id del alumno y la extensión de la imagen
        nombreImagen = 'alumnos/imagenes_perfil/' + str(999) + '.jpg'

        print colored(request.imagen, 'blue')
        urlImagenAlumno = ManejadorImagenes.CreateFile(nombreImagen, request.imagen)

        print urlImagenAlumno

        return mensajesSBD.StatusID(status='test', idEntidad=999)

    #### possibly deprecated ####
    @endpoints.method( mensajesSBD.AlumnoCompleto,  mensajesSBD.MensajeRespuesta, path='alumnos/insertarAlumno', http_method='POST', name='alumnos.insertarAlumno')
    def insertar_alumno(self, request):
        '''
        insertarAlumno()  [POST con todos los atributos de un alumno]

        Introduce un nuevo alumno en el sistema.

        Ejemplo de llamada en terminal:
        curl -i -d "nombre=Juan&dni=45301218Z&direccion=Calle&localidad=Jerezfrontera&provincia=Granada&fecha_nacimiento=1988-2-6&telefono=699164459" -X POST -G localhost:8001/_ah/api/helloworld/v1/alumnos/insertarAlumno
        (-i para ver las cabeceras)

        '''

        if v:
            print nombreMicroservicio
            print "Petición POST a alumnos.insertarAlumno"
            print "Contenido de la petición:"
            print str(request)
            print '\n'

        #Si no tenemos todos los atributos entonces enviamos un error de bad request.
        if request.nombre==None or request.apellidos==None or request.dni==None or request.direccion==None or request.localidad==None or request.provincia==None or request.fecha_nacimiento==None or request.telefono==None:
            raise endpoints.BadRequestException('Peticion erronea, faltan datos.')

        #Conformamos la dirección:
        url = "http://%s/" % modules.get_hostname(module=sbd)
        #Añadimos el servicio al que queremos conectarnos.
        url+="alumnos"

        #Extraemos lo datos de la petición al endpoints
        form_fields = {
          "nombre": formatTextInput(request.nombre),
          "apellidos": formatTextInput(request.apellidos),
          "dni": request.dni,
          "direccion": formatTextInput(request.direccion),
          "localidad": formatTextInput(request.localidad),
          "provincia": formatTextInput(request.provincia),
          "fecha_nacimiento": request.fecha_nacimiento,
          "telefono": request.telefono
        }

        if request.imagen != None:
            print 'Hay imagen recibida en insertarAlumno()'
            form_fields['imagen'] = request.imagen
            print form_fields


        if v:
            print "Llamando a: "+url
            print 'DATOS'
            print form_fields


        #Doc de urlfetch: https://cloud.google.com/appengine/docs/python/refdocs/google.appengine.api.urlfetch
        form_data = urllib.urlencode(form_fields)
        #Realizamos la petición al servicio con los datos pasados al endpoint
        result = urlfetch.fetch(url=url, payload=form_data, method=urlfetch.POST)


        #Infro después de la petición:
        if v:
            print nombreMicroservicio
            print "Resultado de la petición: "
            print result.content
            print "Código de estado: "
            print result.status_code

        if str(result.status_code) == '404':
            raise endpoints.NotFoundException('Alumno con ID %s ya existe en el sistema.' % (request.dni))

        #return MensajeRespuesta(message="Todo OK man!")
        #Mandamos la respuesta que nos devuelve la llamada al microservicio:
        return MensajeRespuesta(message=result.content)

    ###   métodos de CREDENCIALES       mSBD     ###

    @endpoints.method(mensajesSBD.Login,  mensajesSBD.salidaLogin, path='login/loginUser', http_method='POST', name='login.loginUser' )
    def loginUser(self, request):
        '''
        Comprueba si un usaurio está en elsistema y en caso de estarlo devuelve su rol y su número de identificación.
        curl -d "username=46666&password=46666" -i -X POST -G localhost:8001/_ah/api/helloworld/v1/login/loginUser
        '''

        #Info de seguimiento
        if v:
            print nombreMicroservicio
            print ' Petición POST a login.loginUser'
            print ' Request: \n '+str(request)+'\n'

        #Conformamos la dirección:
        url = "http://%s/" % modules.get_hostname(module=sbd)
        #Añadimos el metodo al que queremos conectarnos.
        url+="comprobarAccesoUsuario"


        #Extraemos lo datos de la petición al endpoints y empaquetamos un dict.
        datos = {
          "username": formatTextInput(request.username),
          "password": formatTextInput(request.password),
        }

        #Petición al microservicio:
        result = urlfetch.fetch(url=url, payload=urllib.urlencode(datos), method=urlfetch.POST)

        json = jsonpickle.decode(result.content)

        if json=='Usuario no encontrado':
            raise endpoints.NotFoundException('Usuario no encontrado')
        else:
            mensajeSalida=salidaLogin(idUser=str(json['idUsuario']), nombre=str(json['nombre']), rol=str(json['rol']))

        #Info de seguimiento
        if v:
            print nombreMicroservicio
            print ' Return: '+str(mensajeSalida)+'\n'


        return mensajeSalida



    ##############################################
    #   métodos de CONTROL DE ESTUDIANTES        #
    #               mServicio SCE                #
    ##############################################


    #@endpoints.method(message_types.VoidMessage, ListaResumenControlAsistencia )
    #def getAllResumenesControlAsistencia(self, request):






    #La url hay que mejorarla no necesita el /insertarControl (se identifica con el método)
    @endpoints.method(mensajesSCE.ControlAsistencia, mensajesSBD.StatusID, path='controlesAsistencia', http_method='POST', name='controles.insertarControlAsistencia')
    def insertarControlAsistencia(self, request):
        '''
        Permite subir una lista de controles de asistencia.

        curl -H "Content-Type: application/json" -X POST -d @ejemploControlAsistencia.json  localhost:8001/_ah/api/helloworld/v1/controlesAsistencia

        Recibe un control de asistencia completo en formato json, ver ejemploControlAsistencia.json para ver ejemplo.

        '''
        #Info de seguimiento
        if v:
            print nombreMicroservicio
            print ' Petición POST a controles.insertarControl'
            print ' Request: \n '
            print colored(request, 'blue')
            print ' Request-CONTROLES: \n '+str(request.microControlesAsistencia)+'\n'


        #Parseo de los datos en formato message de RPC a JSON enviable a los microservicios a través del urlfetch (seguro que hay una forma mas bonita de hacerlo)

        #Creamos un diciconario con una lista dentro llamada controles.
        diccionario = { 'microControlesAsistencia': []}
        """
        Recorremos los micro controles de asistencia que recibimos de la petición.
        """
        for mca in request.microControlesAsistencia:
            #Creamos un diccionario por cada elemento dentro de controles, que es de tipo ControlAsistencia
            tmpDic = {}
            #Extraemos los datos y los insertarmos en el dic
            tmpDic['asistencia'] = mca.asistencia
            tmpDic['retraso'] = mca.retraso
            #tmpDic['retrasoTiempo'] = mca.retrasoTiempo
            tmpDic['retrasoJustificado'] = mca.retrasoJustificado
            tmpDic['retrasoTiempo'] = mca.retrasoTiempo
            tmpDic['uniforme'] = mca.uniforme
            tmpDic['idAlumno'] = mca.idAlumno

            print colored(tmpDic, 'red')

            #Añadimo este tmpDic mca la lista controles del diccionario principal.
            diccionario['microControlesAsistencia'].append(tmpDic)


        #Los tres restantes vienen por la PARTE COMÚN (no en los controles)
        diccionario['idProfesor'] = request.idProfesor
        diccionario['idClase'] = request.idClase
        diccionario['idAsignatura'] = request.idAsignatura
        #A partir de este momento se incrustan en cada control


        print colored(diccionario, 'blue')

        #Usamos la librería json para terminar de darle formato y listo para usar.
        jsonData = json.dumps(diccionario)
        #Fin del proceso de conversión.


        #Conformamos la dirección:
        url = "http://%s/" % modules.get_hostname(module="sce")
        #Añadimos el metodo al que queremos conectarnos.
        url+="controlesAsistencia"

        #Petición al microservicio, pasándole como payload los datos recibidos aquí en el endpoint
        result = urlfetch.fetch(url=url, payload=jsonData, method=urlfetch.POST, headers = {"Content-Type": "application/json"})

        print ' Status code from microservice response: '+str(result.status_code)

        resultJson = jsonpickle.decode(result.content)

        #Info de seguimiento
        if v:
            print nombreMicroservicio
        #print ' Respuesta de controles.insertarControl '+str(result)

        return mensajesSBD.StatusID( status=resultJson['status'] )




    @endpoints.method(mensajesSCE.ParametrosPeticionResumenes, mensajesSCE.ListaResumenesControlesAsistencia, path='resumenesControlesAsistencia', http_method='GET', name='controles.getResumenes')
    def getResumenesControlesAsistenciaConParametros(self, request):
        '''
        Devuelve una lista con todos los resumenes de los controles de estudiantes almacenados en el sistema filtrados
        por cualquiera de los campos.

        curl -X GET localhost:8001/_ah/api/helloworld/v1/resumenesControlesAsistencia?idProfesor=4


        class ResumenControlAsistencia(messages.Message):
            key = messages.StringField(1, required=True)
            fecha = messages.StringField(2)
            idClase = messages.StringField(3)
            nombreClase = messages.StringField(4)
            idAsignatura = messages.StringField(5)
            nombreAsignatura = messages.StringField(6)
            idProfesor = messages.StringField(7)
            nombreProfesor = messages.StringField(8)

        class ListaResumenControlAsistencia(messages.Message):
            resumenes = messages.MessageField(ResumenControlAsistencia, 1, repeated=True)

        #Cuando pedimos los resumenes de los controles de asistencia los podemos pedir usando parámetros o sin ellos.
        class ParametrosPeticionResumen(messages.Message):
            idProfesor = messages.IntegerField(1)
            idAsignatura = messages.IntegerField(2)
            idClase = messages.IntegerField(3)
            fechaHora = messages.StringFiedl(4)

        '''
        #Info de seguimiento
        if v:
            print nombreMicroservicio
            print ' Petición POST a controles.getResumenes'
            print ' Request: \n '+str(request)+'\n'



        #Conformamos la dirección:
        url = "http://%s/" % modules.get_hostname(module="sce")
        url+="resumenesControlesAsistencia"


        #Extraemos los datos pasados a la petición y los empaquetamos en un dict.

        #Creamos un diccionario
        datos = {}

        #Si viene por parámetro el id del profesor lo añadimos al diccionario
        if request.idProfesor != None:
            datos['idProfesor']=request.idProfesor
        #Hacemos lo mismo con el resto:
        if request.idAsignatura != None:
            datos['idAsignatura']=request.idAsignatura
        if request.idClase != None:
            datos['idClase']=request.idClase
        if request.fechaHora != None:
            datos['fechaHora']=request.fechaHora

        #Vemos como queda datos
        print datos

        #Petición al microservicio:
        result = urlfetch.fetch(url=url, payload=urllib.urlencode(datos), method=urlfetch.POST)
        listaResumenes = jsonpickle.decode(result.content)
        print 'Resultado'
        print colored(listaResumenes, 'red')


        resumenesItems= []

        for resumen in listaResumenes:
            print 'RESUMEN'
            print resumen
            print 'nombreClase'
            print resumen.get('nombreClase')


            resumenesItems.append( mensajesSCE.ResumenControlAsistencia( key=int(resumen.get('key')),
                                                             fechaHora=str(resumen.get('fechaHora')),
                                                             idClase=int(resumen.get('idClase')),
                                                             nombreClase=formatText(resumen.get('nombreClase')),
                                                             idAsignatura=int(resumen.get('idAsignatura')),
                                                             nombreAsignatura=formatText(resumen.get('nombreAsignatura')),
                                                             idProfesor=int(resumen.get('idProfesor')),
                                                             nombreProfesor=formatText(resumen.get('nombreProfesor'))
                                                           ))

        # Pequeño delay para pruebas con el css
        import time
        time.sleep(2)


        return mensajesSCE.ListaResumenesControlesAsistencia(resumenes=resumenesItems)



        #return MensajeRespuesta(message="Hola ke ase!")


    #Modificarlo para que pueda llamarse con la url de forma correcta.
    #La url hay que mejorarla, no necesita el /getControl (Se identifica con el método)
    @endpoints.method(mensajesSBD.ID, mensajesSCE.ControlAsistencia, path='controlesAsistencia', http_method='GET', name='controles.getControl')
    def getControlAsistencia(self, request):
        '''

        curl -X GET localhost:8001/_ah/api/helloworld/v1/controlesAsistencia?id=4644337115725824

        Devuelve un control de asistencia completo que se le pide con el id pasado.
        '''
        #Info de seguimiento
        if v:
            print nombreMicroservicio
            print ' Petición POST a controles.getContol'
            print ' Request: \n '+str(request)+'\n'



        #Conformamos la dirección:
        url = "http://%s/" % modules.get_hostname(module="sce")
        url+="controlesAsistencia/"+request.id

        if v:
            print "Llamando a: "+str(url)

        #Petición al microservicio
        result = urlfetch.fetch(url=url, method=urlfetch.GET)

        print "RESULTADO:"+str(result.status_code)

        if str(result.status_code) == '404':
            raise endpoints.NotFoundException('Control de Asistencia con ID %s no existe en el sistema.' % (request.id))

        #Convertimos el json a un objeto python
        controlAsistencia = jsonpickle.decode(result.content)

        print 'controlAsistencia'
        print controlAsistencia

        #Convertirmos este objeto python al mensja de rpc para ser enviado.

        resumenesItems= []

        #Recorremos todos los elementos de la lista 'controles' del diccionario devuelto por el mservicio sce.
        listaControles = []
        for mControl in controlAsistencia['microControlesAsistencia']:
            #print 'mControl'
            #print mControl
            listaControles.append(mensajesSCE.MicroControlAsistencia(
                                                     asistencia=int(mControl['asistencia']),
                                                     retraso=int(mControl['retraso']),
                                                     retrasoTiempo=int(mControl['retrasoTiempo']),
                                                     retrasoJustificado=int(mControl['retrasoJustificado']),
                                                     uniforme=int(mControl['uniforme']),
                                                     nombreAlumno=formatText(mControl['nombreAlumno']),
                                                     idAlumno=int(mControl['idAlumno'])
                                                   ))

        #Una vez que tenemos la lista componemos el mensaje final
        return mensajesSCE.ControlAsistencia(
                                       microControlesAsistencia=listaControles,
                                       idProfesor=int(controlAsistencia['idProfesor']),
                                       idClase=int(controlAsistencia['idClase']),
                                       idAsignatura=int(controlAsistencia['idAsignatura']),
                                       nombreClase=formatText(controlAsistencia['nombreClase']),
                                       nombreAsignatura=formatText(controlAsistencia['nombreAsignatura']),
                                       nombreProfesor=formatText(controlAsistencia['nombreProfesor']),
                                       fechaHora=controlAsistencia['fechaHora']
                                     )

    @endpoints.method(mensajesSBD.ID, mensajesSBD.StatusID, path='controlesAsistencia', http_method='DELETE', name='controles.delControl')
    def delControlAsistencia(self, request):
        """
        Elimina un control de asistencia pasado como
        """
        pass

    ##############################################
    #   Manejo de imágenes                       #
    ##############################################

    @endpoints.method(mensajesSBD.Imagen, mensajesSBD.MensajeRespuesta, path='imagenes/subirImagen', http_method='POST', name='imagenes.subirImagen')
    def subirImagen(self, request):
        """
        Introduce una imagen en el sistema.
        tipo
        idEntidad
        imagen

        """

        # curl -d "nombre=JuanAntonio" -i -X POST -G localhost:8001/_ah/api/helloworld/v1/imagenes/subirImagen

        '''
         (echo -n '{"image": "'; base64 profile.jpg; echo '"}') | curl -H "Content-Type: application/json"  -d @-  localhost:8001/_ah/api/helloworld/v1/imagenes/subirImagen?name=prueba
        '''

        # curl -d "nombre=prueba" -X POST localhost:8001/_ah/api/helloworld/v1/imagenes/subirImagen

        print "\n ##### IMAGEN RECIBIDA EN API ENDPOINTS: #####\n"
        print '\nImagen en CRUDO: \n'
        #print str(request.imagen)

        #import binascii
        #stringBase64 = binascii.b2a_base64(request.imagen)
        print '\nImagen pasada a de Base64 a string: \n'
        #print stringBase64

        #print request.image.decode(encoding='UTF-8')


        print 'URL \n'
        url = ManejadorImagenes.CreateFile(request.tipo+'/'+request.idEntidad, request.imagen)
        print url

        return mensajesSBD.MensajeRespuesta( message=str(url) )

    @endpoints.method(mensajesSBD.URL, mensajesSBD.MensajeRespuesta, path='imagenes/eliminarImagen', http_method='POST', name='imagenes.eliminarImagen')
    def eliminarImagen(self, request):
        '''
        curl -X POST localhost:8001/_ah/api/helloworld/v1/imagenes/eliminarImagen?url=http://localhost:8001/_ah/img/encoded_gs_file:YXBwX2RlZmF1bHRfYnVja2V0L2Zpbm4uanBlZw==
        '''
        print (request.url)
        return MensajeRespuesta( message=ManejadorImagenes.DeleteFile(request.url))


APPLICATION = endpoints.api_server([HelloWorldApi])
