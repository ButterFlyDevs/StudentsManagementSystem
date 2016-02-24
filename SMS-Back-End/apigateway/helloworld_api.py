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
#Para la decodificaciónd e los datos recibidos en JSON desde las APIs
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

class Profesor(message.Message):
    nombre = messages.StringField(1)
    dni = messages.StringField(2)

class ProfesorCompleto(messages.Message):
    nombre = messages.StringField(1)
    dni = messages.StringField(2)
    direccion = messages.StringField(3)
    localidad = messages.StringField(4)
    provincia = messages.StringField(5)
    fecha_nac = messages.StringField(6)
    telefonoA = messages.StringField(7)
    telefonoB = messages.StringField(8)

class ListaProfesores(messages.Message):
    profesores = messages.MessageField(Profesor, 1, repeated=True)

class Asignatura(messages.Message):
    id = messages.StringField(1)
    nombre = messages.StringField(2)

class ListaAsignaturas(messages.Message):
    asignaturas = messages.MessageField(Asignatura, 1, repeated=True)

class Curso(messages.Message):
    id = messages.StringField(1)
    curso = messages.StringField(2)
    grupo = messages.StringField(3)
    nivel = messages.StringField(4)

class ListaCursos(messages.Message):
    cursos = messages.MessageField(Curso, 1, repeated=True)


#Decorador que establace nombre y versión de la api
@endpoints.api(name='helloworld', version='v1')

class HelloWorldApi(remote.Service):
    """Helloworld API v1."""

    ##############################################
    #   COLECCIÓN ALUMNOS      /alumnos          #
    ##############################################

    '''
    getAlumnos()   [GET sin parámetros]

    Devuelve una lista con todos los estudiantes registrados en el sistema, de forma simplificada (solo nombre y DNI)

    Llamada desde terminal:
    curl -X GET localhost:8001/_ah/api/helloworld/v1/alumnos/getAlumnos
    Llamada desde JavaScript:
    response =service.alumnos().getAlumnos().execute()
    '''
    @endpoints.method(message_types.VoidMessage, ListaAlumnos,
                      #path=nombre del recurso a llamar
                      path='alumnos/getAlumnos', http_method='GET',
                      #Puede que sea la forma en la que se llama desde la api:
                      #response = service.alumnos().listGreeting().execute()
                      name='alumnos.getAlumnos')
    def getAlumnos(self, unused_request):
        #Transformación de la llamada al endpoints a la llamada a la api rest del servicio.

        print ("Llamando a una función específica")

        #Conexión a un microservicio específico:

        module = modules.get_current_module_name()
        instance = modules.get_current_instance_id()

        #Le decimos a que microservicio queremos conectarnos (solo usando el nombre del mismo), GAE descubre su URL solo.
        url = "http://%s/" % modules.get_hostname(module="microservicio1")
        #Añadimos el recurso al que queremos conectarnos.
        url+="alumnos"
        print str(url)
        #result = urllib2.urlopen(url)
        #print result

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

        #Los adaptamos al tipo de mensaje y enviamos
        #return Greeting(message=str(result.content))
        return ListaAlumnos(alumnos=alumnosItems)


    '''
    getAlumno() [GET con dni]

    Devuelve toda la información de un estudiante en caso de estar en el sistema.

    Llamada ejemplo desde terminal:
    curl -X GET localhost:8001/_ah/api/helloworld/v1/alumnos/getAlumno?dni=11AA22BBZ
    '''

    @endpoints.method(DNI, AlumnoCompleto, path='alumnos/getAlumno', http_method='GET', name='alumnos.getAlumno')
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
    insertarAlumno()  [POST con todos los atributos de un alumno]

    Introduce un nuevo alumno en el sistema.

    Ejemplo de llamada en terminal:
    curl -i -d "nombre=Juan&dni=45301218Z&direccion=Calle&localidad=Jerezfrontera&provincia=Granada&fecha_nac=1988-2-6&telefono=699164459" -X POST -G localhost:8001/_ah/api/helloworld/v1/alumnos/insertarAlumno
    (-i para ver las cabeceras)

    '''
    @endpoints.method(AlumnoCompleto,MensajeRespuesta,
                     path='insertarAlumno', http_method='POST',
                     name='alumnos.insertarAlumno')
    def insertar_alumno(self, request):

        print "POST EN CLOUDPOINTS"
        #La capacidad de recoger datos desde request vendrá dada por tipo de
        #objeto que se espera como petición, en este caso podrán obtenerse
        #todos los atributos que se hayan definido en AlumnoCompleto

        if v:
            print "Contenido de petición a insertar"
            print str(request)

        #Si no tenemos todos los atributos entonces enviamos un error de bad request.
        if request.nombre==None or request.dni==None or request.direccion==None or request.localidad==None or request.provincia==None or request.fecha_nac==None or request.telefono==None:
            raise endpoints.BadRequestException('Peticion erronea, faltan datos.')

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


        if v:
            print "RESULTADOS DE PETICION AL M1: "
            print result.content
            print result.status_code

        if str(result.status_code) == '404':
            raise endpoints.NotFoundException('Alumno con DNI %s ya existe en el sistema.' % (request.dni))

        #return MensajeRespuesta(message="Todo OK man!")
        #Mandamos la respuesta que nos devuelve la llamada al microservicio:
        return MensajeRespuesta(message=result.content)

    '''

    delAlumno()  [DELETE con dniAlumno]

    #Ejemplo de borrado de un recurso pasando el dni de un alumno
    Ubuntu> curl -d "dni=1" -X DELETE -G localhost:8001/_ah/api/helloworld/v1/alumnos/eliminaralumno
    {
     "message": "OK"
    }

    #Ejemplo de ejecución en el caso de no encontrar el recurso:
    Ubuntu> curl -d "dni=1" -X DELETE -G localhost:8001/_ah/api/hellworld/v1/alumnos/eliminaralumno
    {
     "message": "Elemento no encontrado"
    }
    '''

    @endpoints.method(DNI,MensajeRespuesta,path='delAlumno', http_method='DELETE', name='alumnos.delAlumno')
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


    '''
    Devuelve una lista con los datos completos de los profesores que dan clase al alumno de dni pasado
    curl -i -X GET localhost:8001/_ah/api/helloworld/v1/alumnos/getProfesoresAlumno?dni=1
    '''
    @endpoints.method(DNI, ListaProfesores, path='alumnos/getProfesoresAlumno', http_method='GET', name='alumnos.getProfesoresAlumno')
    def getProfesoreAlumno(self, request):
        #Transformación de la llamada al endpoints a la llamada a la api rest del servicio.
        if v:
            print ("Ejecución de getProfesoresAlumno en apigateway")

        #Conexión a un microservicio específico:

        module = modules.get_current_module_name()
        instance = modules.get_current_instance_id()
        #Le decimos a que microservicio queremos conectarnos (solo usando el nombre del mismo), GAE descubre su URL solo.
        url = "http://%s/" % modules.get_hostname(module="microservicio1")

        #Añadimos a la url la coleccion (alumnos), el recurso (alumno dado por su dni) y el recurso anidado de este (profesores)
        url+='alumnos/'+request.dni+"/profesores"

        #Realizamos la petición
        result = urlfetch.fetch(url)

        #Vamos a intentar consumir los datos en JSON y convertirlos a un mensje enviable :)

        print "IMPRESION DE LOS DATOS RECIBIDOS"
        print result.content
        listaProfesores = jsonpickle.decode(result.content)

        #Creamos un vector
        profesoresItems= []
        #Que rellenamos con todo los alumnos de la listaAlumnos
        for profesor in listaProfesores:
            profesoresItems.append(ProfesorCompleto( nombre=str(profesor.get('nombre')),
                                           dni=str(profesor.get('dni')),
                                           direccion=str(profesor.get('direccion')),
                                           localidad=str(profesor.get('localidad')),
                                           provincia=str(profesor.get('provincia')),
                                           fecha_nac=str(profesor.get('fecha_nac')),
                                           telefonoA=str(profesor.get('telefonoA')),
                                           telefonoB=str(profesor.get('telefonoB'))
                                         )
                                )

        #Los adaptamos al tipo de mensaje y enviamos
        #return Greeting(message=str(result.content))
        return ListaProfesores(profesores=profesoresItems)


    '''
    Devuelve una lista con los datos completos de las asignatuas en las que está matriculado el alumno con dni pasado.
    Ejemplo de llamada:
    > curl -i -X GET localhost:8001/_ah/api/helloworld/v1/alumos/getAsignaturasAlumno?dni=1
    '''
    @endpoints.method(DNI, ListaAsignaturas, path='alumnos/getAsignaturasAlumno', http_method='GET', name='alumnos.getAsignaturasAlumno')
    def getAsignaturasAlumno(self, request):
        if v:
            print ("Ejecución de getAsignaturasAlumno en apigateway")
        module = modules.get_current_module_name()
        instance = modules.get_current_instance_id()
        url = "http://%s/" % modules.get_hostname(module="microservicio1")
        url+='alumnos/'+request.dni+"/asignaturas"
        result = urlfetch.fetch(url)
        if v:
            print result.content
        listaAsignaturas = jsonpickle.decode(result.content)
        print listaAsignaturas
        asignaturasItems= []
        for asignatura in listaAsignaturas:
            asignaturasItems.append( Asignatura( id=str(asignatura.get('id')), nombre=str(asignatura.get('nombre')) ) )
        return ListaAsignaturas(asignaturas=asignaturasItems)


    '''
    Devuelve una lista con los datos completos de las cursos en las que está matriculado el alumno con dni pasado.
    Ejemplo de llamada:
    > curl -i -X GET localhost:8001/_ah/api/helloworld/v1/alumos/getCursosAlumno?dni=1
    '''
    @endpoints.method(DNI, ListaCursos, path='alumnos/getCursosAlumno', http_method='GET', name='alumnos.getCursosAlumno')
    def getCursosAlumno(self, request):
        if v:
            print ("Ejecución de getCursosAlumno en apigateway")
        module = modules.get_current_module_name()
        instance = modules.get_current_instance_id()
        url = "http://%s/" % modules.get_hostname(module="microservicio1")
        url+='alumnos/'+request.dni+"/cursos"
        result = urlfetch.fetch(url)
        if v:
            print result.content
        listaCursos = jsonpickle.decode(result.content)
        print listaCursos
        cursosItems= []
        for curso in listaCursos:
            cursosItems.append(Curso(id=str(curso.get('id')),curso=str(curso.get('nombre')),grupo=str(curso.get('grupo')),nivel=str(curso.get('nivel'))))
        return ListaCursos(cursos=cursosItems)



    ##############################################
    #   FUNCIONES PARA ENTIDADES PROFESORES      #
    ##############################################


    @endpoints.method(message_types.VoidMessage, ListaProfesores,
                      path='profesores/getProfesores', http_method='GET',
                      name='profesores.getProfesores')
    def getProfesores(self, unused_request):
        '''
        Devuelve una lista con todos los profesores registrados en el sistema, de forma simplificada (solo nombre y DNI)

        Llamada desde terminal:
        curl -X GET localhost:8001/_ah/api/helloworld/v1/profesores/getProfesores
        Llamada desde JavaScript:
        response =service.profesores.getProfesores().execute()
        '''
        #Identificación del módulo en el que estamos.
        module = modules.get_current_module_name()
        instance = modules.get_current_instance_id()

        #Le decimos a que microservicio queremos conectarnos (solo usando el nombre del mismo), GAE descubre su URL solo.
        url = "http://%s/" % modules.get_hostname(module="microservicio1")
        #Añadimos el recurso al que queremos conectarnos.
        url+="profesores"
        if v:
            print str(url)
        #Al no especificar nada se llama al método GET de la URL.
        result = urlfetch.fetch(url)
        if v:
            print result.content
        listaProfesores = jsonpickle.decode(result.content)

        #Creamos un vector
        profesoresItems= []
        #Que rellenamos con todo los profesores de la listaProfesores
        for profesore in listaProfesores:
            profesoresItems.append(Profesor( nombre=str(alumno.get('nombre')), dni=str(alumno.get('dni'))  ))

        #Los adaptamos al tipo de mensaje y enviamos
        #return Greeting(message=str(result.content))
        return ListaAlumnos(alumnos=alumnosItems)















APPLICATION = endpoints.api_server([HelloWorldApi])
