# -*- coding: utf-8 -*-
"""Hello World API implemented using Google Cloud Endpoints.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""


import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
import os

##Doc de urlfetch: https://cloud.google.com/appengine/docs/python/refdocs/google.appengine.api.urlfetch
##Librerías usadas para la llamada a las APIRest de los microservicios
from google.appengine.api import urlfetch
import urllib

#Para el descubrimiento de los módulos
import urllib2
from google.appengine.api import modules


import jsonpickle
#Variable habilitadora del modo verbose
v=True

# TODO: Replace the following lines with client IDs obtained from the APIs
# Console or Cloud Console.
WEB_CLIENT_ID = 'replace this with your web client application ID'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID


package = 'Hello'



class MensajeRespuesta(messages.Message):
    message = messages.StringField(1)


class MensajePeticion(messages.Message):
    message = messages.StringField(1)
'''
Como vemos, no aparecen argumentos en el cuerpo de la petición ya que se trata
de una petición de tipo GET.
'''

#######################################
# TIPOS DE MENSAJES QUE MANEJA LA API #
#######################################

class Alumno(messages.Message):
    nombre = messages.StringField(1)
    dni = messages.StringField(2)

class AlumnoCompleto(messages.Message):
    nombre = messages.StringField(1)
    dni = messages.StringField(2)
    direccion = messages.StringField(3)
    localidad = messages.StringField(4)
    provincia = messages.StringField(5)
    fecha_nac = messages.StringField(6)
    telefono = messages.StringField(7)




class DNI(messages.Message):
    dni = messages.StringField(1)

class ListaAlumnos(messages.Message):
    alumnos = messages.MessageField(Alumno, 1, repeated=True)


class Greeting(messages.Message):
    """Greeting that stores a message."""
    message = messages.StringField(1)

class GreetingCollection(messages.Message):
    """Collection of Greetings."""
    items = messages.MessageField(Greeting, 1, repeated=True)


STORED_GREETINGS = GreetingCollection(items=[
    Greeting(message='hello world!'),
    Greeting(message='goodbye world!'),
])


@endpoints.api(name='helloworld', version='v1')

class HelloWorldApi(remote.Service):
    """Helloworld API v1."""

    MULTIPLY_METHOD_RESOURCE = endpoints.ResourceContainer(
            Greeting,
            times=messages.IntegerField(2, variant=messages.Variant.INT32,
                                        required=True))

    @endpoints.method(MULTIPLY_METHOD_RESOURCE, Greeting,
                      path='hellogreeting/{times}', http_method='POST',
                      name='greetings.multiply')


    def greetings_multiply(self, request):
        return Greeting(message=request.message * request.times)


#########  INTENTO DE IMPLEMENTACIÓN DE UN METODO DELETE para eliminar un alumno


    '''
    #Ejemplo de borrado de un recurso pasando el dni de un alumno
    Ubuntu> curl -d "dni=1" -X DELETE -G localhost:8001/_ah/api/helloworld/v1/eliminaralumno
    {
     "message": "OK"
    }

    #Ejemplo de ejecución en el caso de no encontrar el recurso:
    Ubuntu> curl -d "dni=1" -X DELETE -G localhost:8001/_ah/api/hellworld/v1/eliminaralumno
    {
     "message": "Elemento no encontrado"
    }
    '''

    @endpoints.method(DNI,MensajeRespuesta,
                     path='delAlumno', http_method='DELETE',
                     name='greetings.delAlumno')
    def eliminar_alumno(self, request):

        print "POST EN CLOUDPOINTS"
        print str(request)

        #Una vez que tenemos los datos aquí los enviamos al servicio que gestiona la base de datos.
        #Podemos imprimir por pantalla los datos recolectados
        print "MENSAJE RECIBIDO EN ENDPOINTS"+request.dni

        #Nos conectamos al modulo para enviarle los mismos
        from google.appengine.api import modules
        #Conformamos la dirección:
        url = "http://%s/" % modules.get_hostname(module="microservicio1")
    
        '''
        Parece que urlfetch da problemas a al hora de pasar parámetros (payload) cuando se trata del
        método DELETE.
        Extracto de la doc:
        payload: POST, PUT, or PATCH payload (implies method is not GET, HEAD, or DELETE). this is ignored if the method is not POST, PUT, or PATCH.
        Además no somos los primeros en encontrarse este problema:
        http://grokbase.com/t/gg/google-appengine/13bvr5qjyq/is-there-any-reason-that-urlfetch-delete-method-does-not-support-a-payload

        Según la última cuestión puede que tengamos que usar POST

        '''
        url+='alumnos/'+request.dni

        #EL problema queda aquí, a expensas de ver si podemos usar DELETE o tenemos que realizar un apaño con post
        #usando algún parámetro que indique si se debe eliminar.
        result = urlfetch.fetch(url=url, method=urlfetch.DELETE)

        print "RESULTADOS DE PETICION AL M1: "
        print result.content

        #return MensajeRespuesta(message="Todo OK man!")
        #Mandamos la respuesta que nos devuelve la llamada al microservicio:
        return MensajeRespuesta(message=result.content)

######### FIN DE INTENTO










    ############################
    #   COLECCIÓN ALUMNOS      #
    ############################

    '''
    getAlumnos()   [GET sin parámetros]

    Devuelve una lista con todos los estudiantes registrados en el sistema.

    Llamada desde terminal:
    curl -X GET localhost:8001/_ah/api/helloworld/v1/getAlumnos
    Llamada desde JavaScript:
    response =service.greetings().getAlumnos().execute()
    '''
    @endpoints.method(message_types.VoidMessage, ListaAlumnos,
                      #path=nombre del recurso a llamar
                      path='getAlumnos', http_method='GET',
                      #Puede que sea la forma en la que se llama desde la api:
                      #response = service.greetings().listGreeting().execute()
                      name='greetings.getAlumnos')
    def getAlumnos(self, unused_request):
        #Transformación de la llamada al endpoints a la llamada a la api rest del servicio.

        print ("Llamando a una función específica")

        #Conexión a un microservicio específico:

        from google.appengine.api import modules
        module = modules.get_current_module_name()
        instance = modules.get_current_instance_id()
        import urllib2
        from google.appengine.api import modules

        #Le decimos a que microservicio queremos conectarnos (solo usando el nombre del mismo), GAE descubre su URL solo.
        url = "http://%s/" % modules.get_hostname(module="microservicio1")
        #Añadimos el recurso al que queremos conectarnos.
        url+="alumnos"
        print str(url)
        #result = urllib2.urlopen(url)
        #print result

        #Envío de su resultado
        from google.appengine.api import urlfetch

        #Llamamos al microservicio y recibimos los resultados con URLFetch
        #Al no especificar nada se llama al método GET de la URL.
        result = urlfetch.fetch(url)

        #Vamos a intentar consumir los datos en JSON y convertirlos a un mensje enviable :)

        print "IMPRESION DE LOS DATOS RECIBIDOS"
        print result.content
        listaAlumnos = jsonpickle.decode(result.content)

        for alumno in listaAlumnos:
            print "nombre: "+str(alumno.get('nombre'))
            print "dni: "+str(alumno.get('dni'))

        '''
        miListaAlumnos=ListaAlumnos()
        miListaAlumnos.alumnos = listaAlumnos
        '''

        #Creamos un vector
        alumnosItems= []
        #Que rellenamos con todo los alumnos de la listaAlumnos
        for alumno in listaAlumnos:
            alumnosItems.append(Alumno( nombre=str(alumno.get('nombre')), dni=str(alumno.get('dni'))  ))

        '''
        greetingItems.append(Greeting(message='hello world2'))
        greetingItems.append(Greeting(message='goodbye world2'))
        STORED_GREETINGS2=GreetingCollection(items=greetingItems)
        '''

        #Los adaptamos al tipo de mensaje y enviamos
        #return Greeting(message=str(result.content))
        return ListaAlumnos(alumnos=alumnosItems)


    '''
    getAlumno() [GET con dni]

    Devuelve toda la información de un estudiante en caso de estar en el sistema.

    Llamada ejemplo desde terminal:
    curl -X GET localhost:8001/_ah/api/helloworld/v1/getAlumno?dni=11AA22BBZ
    '''

    @endpoints.method(DNI, AlumnoCompleto, path='getAlumno', http_method='GET', name='greetings.getAlumno')
    def getAlumno(self,request):
        print "GET CON PARÁMETROS EN ENDPOINT"

        #Cuando se llama a este recurso lo que se quiere es recibir toda la información
        #de una entidad Alumno, para ello primero vamos a recuperar la información del microsrevicio apropiado:

        #Conexión a un microservicio específico:
        module = modules.get_current_module_name()
        instance = modules.get_current_instance_id()

        #Le decimos al microservicio que queremos conectarnos (solo usando el nombre del mismo), GAE descubre su URL solo.
        url = "http://%s/" % modules.get_hostname(module="microservicio1")

        '''
        Según la doc. de urlfetch (ver arriba) no podemos pasar parámetros con el payload, así que como conocemos
        la api del microservicios al que vamos a llamr realizamos la petición bajo su especificacion, según la cual
        solo tenemos que llamar a /alumnos/<id_alumno> entonces concatenamos a la url esa id qu recibimos en la llamada
        a este procedimiento.
        '''
        #Recursos más entidad
        url+='alumnos/'+request.dni

        if v:
            print "calling: "+ url

        #Petición al microservicio
        result = urlfetch.fetch(url=url, method=urlfetch.GET)

        print "RESULTADO:"+str(result.status_code)
        #print result.content
        if v:
            print result.status_code
        if str(result.status_code) == '400':
            raise endpoints.BadRequestException('Peticion erronea')

        if str(result.status_code) == '404':
            raise endpoints.NotFoundException('Alumno con DNI %s no encontrado.' % (request.dni))

        alumno = jsonpickle.decode(result.content)

        return AlumnoCompleto(nombre=alumno.get('nombre'),
                                 dni=alumno.get('dni'),
                                 direccion=alumno.get('direccion'),
                                 localidad=alumno.get('localidad'),
                                 provincia=alumno.get('provincia'),
                                 fecha_nac=str(alumno.get('fecha_nac')),
                                 telefono=alumno.get('telefono')
                                )


















    '''
    /alumnos POST

    Introduce un dnuevo alumno en el sistema.

    '''
    @endpoints.method(AlumnoCompleto,MensajeRespuesta,
                     path='alumnos', http_method='POST',
                     name='greetings.insertaralumno')
    def insertar_alumno(self, request):

        print "POST EN CLOUDPOINTS"
        #La capacidad de recoger datos desde request vendrá dada por tipo de
        #objeto que se espera como petición, en este caso podrán obtenerse
        #todos los atributos que se hayan definido en AlumnoCompleto
        print str(request)
        print "fin"

        #Una vez que tenemos los datos aquí los enviamos al servicio que gestiona la base de datos.
        #Podemos imprimir por pantalla los datos recolectados

        #Nos conectamos al modulo para enviarle los mismos
        from google.appengine.api import modules
        #Conformamos la dirección:
        url = "http://%s/" % modules.get_hostname(module="microservicio1")
        #Añadimos el servicio al que queremos conectarnos.
        url+="alumnos"

        print url

        from google.appengine.api import urlfetch
        import urllib

        #Si algun dato no es pasado se introduce None

        #Extraemos lo datos de la petición al endpoints
        form_fields = {
          "nombre": request.nombre,
          "dni": request.dni,
          "direccion": request.direccion,
          "localidad": request.localidad,
          "provincia": request.provincia,
          "fecha_nac": request.fecha_nac,
          "telefono": request.telefono
        }

        ##Doc de urlfetch: https://cloud.google.com/appengine/docs/python/refdocs/google.appengine.api.urlfetch
        form_data = urllib.urlencode(form_fields)
        #Realizamos la petición al servicio con los datos pasados al endpoint
        result = urlfetch.fetch(url=url, payload=form_data, method=urlfetch.POST)

        print "RESULTADOS DE PETICION AL M1: "
        #print result.content

        #return MensajeRespuesta(message="Todo OK man!")
        #Mandamos la respuesta que nos devuelve la llamada al microservicio:
        return MensajeRespuesta(message=result.content)
















##################




    ID_RESOURCE = endpoints.ResourceContainer(
            message_types.VoidMessage,
            id=messages.IntegerField(1, variant=messages.Variant.INT32))


    @endpoints.method(ID_RESOURCE, Greeting,
                      path='hellogreeting/{id}', http_method='GET',
                      name='greetings.getGreeting')


    def greeting_get(self, request):
        try:
            return STORED_GREETINGS.items[request.id]
        except (IndexError, TypeError):
            raise endpoints.NotFoundException('Greeting %s not found.' %
                                              (request.id,))

    @endpoints.method(message_types.VoidMessage, Greeting,
                      path='hellogreeting/authed', http_method='POST',
                      name='greetings.authed')
    def greeting_authed(self, request):
        current_user = endpoints.get_current_user()
        email = (current_user.email() if current_user is not None
                 else 'Anonymous')
        return Greeting(message='hello %s' % (email,))


APPLICATION = endpoints.api_server([HelloWorldApi])
