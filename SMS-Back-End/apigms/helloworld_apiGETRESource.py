# -*- coding: utf-8 -*-
"""

Hello World API implemented using Google Cloud Endpoints.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.

Para ver el servidor de exploración:

    https://your_app_id.appspot.com/_ah/api/explorer


 > Estandar de log por terminal <

 Intentamos que el código tenga la mayor depuración posible por terminal ya que son tantos pasos de mensajes
 que es más fácil de detectar errores así. Existe una variable v=1 (por defecto) que habilita todos los mensajes y se sigue
 un estandar más o menos regular.

 Cuando se realiza la llamada a un método de la api se añade justo a la entrada el bloque (ajustado al método):

     #Info de seguimiento
     if v:
         print nombreMicroservicio
         print ' Petición GET a profesores.getProfesor'
         print ' Request: \n '+str(request)+'\n'

 y para conocer la salida otro que siga el formato:

     #Info de seguimiento
     if v:
         print nombreMicroservicio
         print ' Return: '+str(profesor)+'\n'

 para saber a que método se ha llamado y con qué parámetros.

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

class MensajeRespuesta(messages.Message):
    message = messages.StringField(1)

#Mensaje que usamos para devolver la información de estado sobre la creación de alguna entidad en el sistema y además devuelve el id en sistema de la identidad creada. (Como por ejemplo en la insercción de un alumno)
class StatusID(messages.Message):
    status = messages.StringField(1)
    statusCode = messages.StringField(2)
    id = messages.IntegerField(3)


class AsignaturaCompleta(messages.Message):
    id = messages.IntegerField(1)



#Decorador que establace nombre y versión de la api
@endpoints.api(name='helloworld', version='v1')
class HelloWorldApi(remote.Service):
    """Helloworld API v1."""


    @endpoints.method(message_types.VoidMessage, MensajeRespuesta, path='holaMundo', http_method='GET', name='holaMundo')
    def getSaludoHolaMundo(self, request):
        '''
        Función de prueba de exposición.
        curl -X GET localhost:8001/_ah/api/helloworld/v1/holaMundo
        '''
        return MensajeRespuesta(message='Hola mundo! \n')



    """
    GET_RESOURCE = endpoints.ResourceContainer(
            # The request body should be empty.
            message_types.VoidMessage,
            # Accept one url parameter: and integer named 'id'
            id=messages.IntegerField(1, variant=messages.Variant.INT32))
    """
    @endpoints.method(AsignaturaCompleta, StatusID, path='asignaturas/insertarAsignatura', http_method='POST', name='asignaturas.insertarAsignatura')
    def insertarAsignatura(self, request):
        '''
        Introduce un nuevo profesor en el sistema.

        Ejemplo de llamada en terminal:
        curl -i -d "nombre=CienciasExperimentales" -X POST -G localhost:8001/_ah/api/helloworld/v1/asignaturas/insertarAsignatura
        '''
        return StatusID(status='242')



APPLICATION = endpoints.api_server([HelloWorldApi])
