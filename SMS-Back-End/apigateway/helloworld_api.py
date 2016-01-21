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

import jsonpickle


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


#########  INTENTO DE IMPLEMENTACIÓN DE UN METODO POST

    @endpoints.method(Alumno,MensajeRespuesta,
                     path='nuevoalumno', http_method='POST',
                     name='greetings.insertaralumno')
    def insertar_alumno(self, request):

        print "POST EN CLOUDPOINTS"
        print str(request)

        #Una vez que tenemos los datos aquí los enviamos al servicio que gestiona la base de datos.
        #Podemos imprimir por pantalla los datos recolectados
        print request.nombre
        print request.dni

        #Nos conectamos al modulo para enviarle los mismos
        from google.appengine.api import modules
        #Conformamos la dirección:
        url = "http://%s/" % modules.get_hostname(module="microservicio1")
        #Añadimos el servicio al que queremos conectarnos.
        url+="alumnos"


        from google.appengine.api import urlfetch
        import urllib

        form_fields = {
          "nombre": request.nombre,
          "dni": request.dni,
        }

        ##Doc de urlfetch: https://cloud.google.com/appengine/docs/python/refdocs/google.appengine.api.urlfetch
        form_data = urllib.urlencode(form_fields)
        result = urlfetch.fetch(url=url, payload=form_data, method=urlfetch.POST)

        print "RESULTADOS DE PETICION AL M1: "
        print result.content

        #return MensajeRespuesta(message="Todo OK man!")
        #Mandamos la respuesta que nos devuelve la llamada al microservicio:
        return MensajeRespuesta(message=result.content)

######### FIN DE INTENTO

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

    @endpoints.method(Alumno,MensajeRespuesta,
                     path='eliminaralumno', http_method='DELETE',
                     name='greetings.eliminaralumno')
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
        #Añadimos el servicio al que queremos conectarnos.
        url+="alumnos"



        from google.appengine.api import urlfetch
        import urllib

        form_fields = {
          "dni": request.dni,
        }

        ##Doc de urlfetch: https://cloud.google.com/appengine/docs/python/refdocs/google.appengine.api.urlfetch
        form_data = urllib.urlencode(form_fields)

        '''
        Parece que urlfetch da problemas a al hora de pasar parámetros (payload) cuando se trata del
        método DELETE.
        Extracto de la doc:
        payload: POST, PUT, or PATCH payload (implies method is not GET, HEAD, or DELETE). this is ignored if the method is not POST, PUT, or PATCH.
        Además no somos los primeros en encontrarse este problema:
        http://grokbase.com/t/gg/google-appengine/13bvr5qjyq/is-there-any-reason-that-urlfetch-delete-method-does-not-support-a-payload

        Según la última cuestión puede que tengamos que usar POST

        '''

        url+='?dni='+request.dni

        #EL problema queda aquí, a expensas de ver si podemos usar DELETE o tenemos que realizar un apaño con post
        #usando algún parámetro que indique si se debe eliminar.
        result = urlfetch.fetch(url=url, method=urlfetch.DELETE)

        print "RESULTADOS DE PETICION AL M1: "
        print result.content

        #return MensajeRespuesta(message="Todo OK man!")
        #Mandamos la respuesta que nos devuelve la llamada al microservicio:
        return MensajeRespuesta(message=result.content)

######### FIN DE INTENTO




    ### PRUEBA DE LLAMADA A ENDPOINT A MÉTODO GET CON PARÁMETROS

    # Se podría llamar así:
    # curl -X GET localhost:8001/_ah/api/helloworld/v1/alumnos?dni=9

    '''
    Ejemplo de llamada correcta:
    Ubuntu> curl -X GET localhost:8001/_ah/api/helloworld/v1/alumnosdni=4
    {
     "direccion": "Direccion4",
     "dni": "4",
     "fecha_nac": "1988-10-05",
     "localidad": "Localidad4",
     "nombre": "Alumno4",
     "provincia": "Provincia4",
     "telefono": "4444"
     }
     Ejemplo de una llamada fallida:
     Ubuntu> curl -X GET localhost:8001/_ah/api/helloworld/v1/alumnosdni=5
    {
     "error": {
      "code": 404,
      "errors": [
       {
        "domain": "global",
        "message": "Alumno con DNI 5 no encontrado.",
        "reason": "notFound"
       }
      ],
      "message": "Alumno con DNI 5 no encontrado."
     }
    '''
    @endpoints.method(DNI, AlumnoCompleto, path='alumnos', http_method='GET', name='greetings.getAlumno')
    def getAlumno(self,request):
        print "GET CON PARÁMETROS EN ENDPOINT"

        #Cuando se llama a este recurso lo que se quiere es recibir toda la información
        #de una entidad Alumno, para ello primero vamos a recuperar la información del microsrevicio apropiado:

        #Conexión a un microservicio específico:

        from google.appengine.api import modules
        module = modules.get_current_module_name()
        instance = modules.get_current_instance_id()
        import urllib2
        from google.appengine.api import modules

        #Le decimos al microservicio que queremos conectarnos (solo usando el nombre del mismo), GAE descubre su URL solo.
        url = "http://%s/" % modules.get_hostname(module="microservicio1")
        #Añadimos el recurso al que queremos conectarnos.
        url+="alumnos"

        #Una vez conseguida la url del servicio con el autodescrubrimiento, usamos urlfetch para usar el servicio
        from google.appengine.api import urlfetch
        import urllib

        form_fields = {
          "dni": request.dni,
        }

        ##Doc de urlfetch: https://cloud.google.com/appengine/docs/python/refdocs/google.appengine.api.urlfetch

        #GET tampoco permite pasar parámetros, cosa que se entiende!!

        '''
        Una solución que podemos tomar es pasar los parámetros en la url.
        '''

        url+='?dni='+request.dni


        try:

            form_data = urllib.urlencode(form_fields)
            result = urlfetch.fetch(url=url, method=urlfetch.GET)
            print "RESULTADOS"
            #print result.content

            alumno = jsonpickle.decode(result.content)

            print "salida de jsonpickle\n"+str(alumno)+'\n'
            if(alumno=="Elemento no encontrado"):
                print "ELEMENTO NO ENCONTRADO"
                #Lo único que estamos haciendo es provocar una excepción de tipo IndexError, a falta de crear las nuestras propias.
                print alumno[10000000]
            #Cogemos el dni pasado por parámetro y lo devolvemos para comprobar que funciona.

            ##
            '''
            Otro problema:
            - Si el alumno se encuentra se devuelve un mensaje de tipo Alumno, pero si no se encuentra
            porque por ejemplo el alumno no está en la base de datos hay que devolver un error entonces el tipo
            de mensaje a devolver cambia. Y no se puede modificar el tipo de dato que devuelve cambiando
            el return porque se especifica en la cabecera lo que se va a devolver.
            ¿Qué hacer?
            1.Buscar la forma de pasar directamente el json como nos venga, con lo cual simplificaríamos todo el paso
            de mensajes al tener sólo un tipo de mensaje, que sería el crudo del json.
            2.Encontrar la manera de enviar dos tipos de mensajes, arreglaríamos esto pero seguiría complicandose el
            endpoint conforme fuera creciendo.

            Preguntar en StackOverflow

            ##
            '''
            #return Alumno(nombre='SALIDA', dni=request.dni)
            #En el caso de que el estudiante se haya encontrado se envía toda la informaicón disponible:
            return AlumnoCompleto(nombre=alumno.get('nombre'),
                                  dni=alumno.get('dni'),
                                  direccion=alumno.get('direccion'),
                                  localidad=alumno.get('localidad'),
                                  provincia=alumno.get('provincia'),
                                  fecha_nac=str(alumno.get('fecha_nac')),
                                  telefono=alumno.get('telefono')
                                 )

        except (IndexError, TypeError):
            raise endpoints.NotFoundException('Alumno con DNI %s no encontrado.' % (request.dni,))
    ###



######################

    '''
    # curl -X GET localhost:8080/_ah/api/helloworld/v1/hellogreeting
    @endpoints.method(message_types.VoidMessage, GreetingCollection,
                      #path=nombre del recurso a llamar
                      path='hellogreeting', http_method='GET',
                      #Puede que sea la forma en la que se llama desde la api:
                      #response = service.greetings().listGreeting().execute()
                      name='greetings.listGreeting')
    def greetings_list(self, unused_request):
        return STORED_GREETINGS
    '''

    @endpoints.method(message_types.VoidMessage, ListaAlumnos,
                      #path=nombre del recurso a llamar
                      path='hellogreeting', http_method='GET',
                      #Puede que sea la forma en la que se llama desde la api:
                      #response = service.greetings().listGreeting().execute()
                      name='greetings.listGreeting')
    def greetings_list(self, unused_request):
        print ("Llamando a una función específica")

        #Conexión a un microservicio específico:

        from google.appengine.api import modules
        module = modules.get_current_module_name()
        instance = modules.get_current_instance_id()
        import urllib2
        from google.appengine.api import modules

        #Le decimos al microservicio que queremos conectarnos (solo usando el nombre del mismo), GAE descubre su URL solo.
        url = "http://%s/" % modules.get_hostname(module="microservicio1")
        #Añadimos el recurso al que queremos conectarnos.
        url+="alumnos"
        print str(url)
        #result = urllib2.urlopen(url)
        #print result

        #Envío de su resultado

        from google.appengine.api import urlfetch

        #Llamamos al microservicio y recibimos los resultados con URLFetch
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

        alumnosItems= []

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
