# -*- coding: utf-8 -*-
"""Hello World API implemented using Google Cloud Endpoints.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""


import endpoints
#https://cloud.google.com/appengine/docs/python/tools/protorpc/messages/messageclass
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

nombreMicroservicio = '\n## API Gateway ##\n'

# TODO: Replace the following lines with client IDs obtained from the APIs
# Console or Cloud Console.
WEB_CLIENT_ID = 'replace this with your web client application ID'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID


package = 'Hello'

def formatText(cadena):
    '''
    Función que recibe una cadena como parámetro y la formatea para resolver el problema de los acentos.
    '''
    return cadena.encode('utf-8').decode('utf-8')

def formatTextInput(cadena):
    return cadena.encode('utf-8')

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
    apellidos = messages.StringField(2)
    id = messages.StringField(3)

class AlumnoCompleto(messages.Message):
    id = messages.StringField(1)
    nombre = messages.StringField(2)
    apellidos = messages.StringField(3)
    dni = messages.StringField(4)
    direccion = messages.StringField(5)
    localidad = messages.StringField(6)
    provincia = messages.StringField(7)
    fecha_nacimiento = messages.StringField(8)
    telefono = messages.StringField(9)
    imagen = messages.StringField(10)

class ID(messages.Message):
    id = messages.StringField(1)

class ListaAlumnos(messages.Message):
    alumnos = messages.MessageField(Alumno, 1, repeated=True)

class Profesor(messages.Message):
    nombre = messages.StringField(1)
    apellidos = messages.StringField(2)
    id = messages.StringField(3)



class ProfesorCompleto(messages.Message):
    id = messages.StringField(1)
    nombre = messages.StringField(2)
    apellidos = messages.StringField(3)
    dni = messages.StringField(4)
    direccion = messages.StringField(5)
    localidad = messages.StringField(6)
    provincia = messages.StringField(7)
    fecha_nacimiento = messages.StringField(8)
    telefono = messages.StringField(9)

class ListaProfesores(messages.Message):
    profesores = messages.MessageField(Profesor, 1, repeated=True)

class Asignatura(messages.Message):
    id = messages.StringField(1)
    nombre = messages.StringField(2)

class AsignaturaCompleta(messages.Message):
    id = messages.StringField(1)
    nombre = messages.StringField(2)

class ListaAsignaturas(messages.Message):
    asignaturas = messages.MessageField(Asignatura, 1, repeated=True)

class Clase(messages.Message):
    id = messages.StringField(1)
    curso = messages.StringField(2)
    grupo = messages.StringField(3)
    nivel = messages.StringField(4)

#Para ampliar en el futuro y no usar el mismo tipo de mensaje:
class ClaseCompleta(messages.Message):
    id = messages.StringField(1)
    curso = messages.StringField(2)
    grupo = messages.StringField(3)
    nivel = messages.StringField(4)

class ListaClases(messages.Message):
    clases = messages.MessageField(Clase, 1, repeated=True)

class Matricula(messages.Message):
    id_matricula = messages.StringField(1)
    id_alumno = messages.StringField(2)
    id_asociacion = messages.StringField(3)

class ListaMatriculas(messages.Message):
    matriculas = messages.MessageField(Matricula, 1, repeated=True)

class Imparte(messages.Message):
    id_imparte = messages.StringField(1)
    id_profesor = messages.StringField(2)
    id_asociacion = messages.StringField(3)

class ListaImpartes(messages.Message):
    impartes = messages.MessageField(Imparte, 1, repeated=True)

class Asociacion(messages.Message):
    id_asociacion = messages.StringField(1)
    id_clase = messages.StringField(2)
    id_asignatura = messages.StringField(3)
    nombreAsignatura = messages.StringField(4)

class ListaAsociaciones(messages.Message):
    asociaciones = messages.MessageField(Asociacion, 1, repeated=True)

#Un nuevo tipo de mensaje para el profesor simple que añade un poco de información necesaria
class ProfesorSimpleExtendido(messages.Message):
    nombre = messages.StringField(1)
    apellidos = messages.StringField(2)
    id = messages.StringField(3)
    idImparte = messages.StringField(4)

class AlumnoSimpleExtendido(messages.Message):
    nombre = messages.StringField(1)
    apellidos = messages.StringField(2)
    id = messages.StringField(3)
    idMatricula = messages.StringField(4)

#Definimos un tipo especial de mensaje
class AsociacionCompleta(messages.Message):
    nombreAsignatura = messages.StringField(1)
    listaProfesores = messages.MessageField(ProfesorSimpleExtendido, 2, repeated=True)
    listaAlumnos = messages.MessageField(AlumnoSimpleExtendido, 3, repeated=True)
    idAsociacion = messages.StringField(4)


#Decorador que establace nombre y versión de la api
@endpoints.api(name='helloworld', version='v1')
class HelloWorldApi(remote.Service):
    """Helloworld API v1."""

    ##############################################
    #   métodos de ALUMNOS                       #
    ##############################################

    @endpoints.method(message_types.VoidMessage, ListaAlumnos,
                      #path=nombre del recurso a llamar
                      path='alumnos/getAlumnos', http_method='GET',
                      #Puede que sea la forma en la que se llama desde la api:
                      #response = service.alumnos().listGreeting().execute()
                      name='alumnos.getAlumnos')
    def getAlumnos(self, unused_request):
        '''
        getAlumnos()   [GET sin parámetros]

        Devuelve una lista con todos los estudiantes registrados en el sistema, de forma simplificada (solo nombre y ID)

        Llamada desde terminal:
        curl -X GET localhost:8001/_ah/api/helloworld/v1/alumnos/getAlumnos
        Llamada desde JavaScript:
        response =service.alumnos().getAlumnos().execute()
        '''
        #Transformación de la llamada al endpoints a la llamada a la api rest del servicio.

        #Info de seguimiento
        if v:
            print nombreMicroservicio
            print "Petición GET a alumnos.getAlumnos"
            print '\n'

        #Conexión a un microservicio específico:

        module = modules.get_current_module_name()
        instance = modules.get_current_instance_id()

        #Le decimos a que microservicio queremos conectarnos (solo usando el nombre del mismo), GAE descubre su URL solo.
        url = "http://%s/" % modules.get_hostname(module="microservicio1")
        #Añadimos el recurso al que queremos conectarnos.
        url+="alumnos"
        #result = urllib2.urlopen(url)
        #print result

        if v:
            print "Llamando a: "+str(url)
        #Llamamos al microservicio y recibimos los resultados con URLFetch
        #Al no especificar nada se llama al método GET de la URL.
        result = urlfetch.fetch(url)

        #Vamos a intentar consumir los datos en JSON y convertirlos a un mensje enviable :)

        if v:
            print nombreMicroservicio
            print "Resultados de la petición: "
            print result.content
            print "Código de estado: "+str(result.status_code)+'\n'

        listaAlumnos = jsonpickle.decode(result.content)

        '''
        miListaAlumnos=ListaAlumnos()
        miListaAlumnos.alumnos = listaAlumnos
        '''

        #Creamos un vector
        alumnosItems= []
        #Que rellenamos con todo los alumnos de la listaAlumnos

        if v:
            print "Construcción del mensaje de salida: \n"

        for alumno in listaAlumnos:
            idAlumno = str(alumno.get('id'))
            nombreAlumno = alumno.get('nombre')
            apellidosAlumno = alumno.get('apellidos')

            alumnosItems.append(Alumno( id=idAlumno, nombre=formatText(nombreAlumno), apellidos=formatText(apellidosAlumno) ) )


        #id=str(alumno.get('id')),
        #Los adaptamos al tipo de mensaje y enviamos
        #return Greeting(message=str(result.content))
        return ListaAlumnos(alumnos=alumnosItems)

    @endpoints.method(ID, AlumnoCompleto, path='alumnos/getAlumno', http_method='GET', name='alumnos.getAlumno')
    def getAlumno(self,request):
        '''
        getAlumno() [GET con dni]

        Devuelve toda la información de un estudiante en caso de estar en el sistema.

        Llamada ejemplo desde terminal:
        curl -X GET localhost:8001/_ah/api/helloworld/v1/alumnos/getAlumno?id=2
        '''

        #Info de seguimiento
        if v:
            print nombreMicroservicio
            print "Petición GET a alumnos.getAlumno"
            print "request: "+str(request)
            print '\n'

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
        url+='alumnos/'+request.id

        if v:
            print "Llamando a: "+str(url)

        #Petición al microservicio
        result = urlfetch.fetch(url=url, method=urlfetch.GET)

        print "RESULTADO:"+str(result.status_code)
        #print result.content
        if v:
            print result.status_code
        if str(result.status_code) == '400':
            raise endpoints.BadRequestException('Peticion erronea')

        if str(result.status_code) == '404':
            raise endpoints.NotFoundException('Alumno con ID %s no encontrado.' % (request.dni))

        alumno = jsonpickle.decode(result.content)

        #Infro después de la petición:
        if v:
            print nombreMicroservicio
            print "Resultado de la petición: "
            print result.content
            print "\nCódigo de estado: "+str(result.status_code)+'\n'




        #Componemos un mensaje de tipo AlumnoCompleto.
        #Las partes que son enteros las pasamos a string para enviarlos como mensajes de tipo string.

        #Ojo, solo los elementos que no sean null se enviarán. Cuando un alumno no tenga imagen y pr tanto su valor
        #en la base de datos sea null no se recibirá el campo imagen en el JSON que la API G devuelve.

        alumno = AlumnoCompleto(id=str(alumno.get('id')),
                                nombre=formatText(alumno.get('nombre')),
                                apellidos=formatText(alumno.get('apellidos')),
                                dni=str(alumno.get('dni')),
                                direccion=formatText(alumno.get('direccion')),
                                localidad=formatText(alumno.get('localidad')),
                                provincia=formatText(alumno.get('provincia')),
                                fecha_nacimiento=str(alumno.get('fecha_nacimiento')),
                                telefono=alumno.get('telefono'),
                                imagen=alumno.get('urlImagen')
                                )

        return alumno

    @endpoints.method(AlumnoCompleto,MensajeRespuesta, path='alumnos/insertarAlumno', http_method='POST', name='alumnos.insertarAlumno')
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
        url = "http://%s/" % modules.get_hostname(module="microservicio1")
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


        ##Doc de urlfetch: https://cloud.google.com/appengine/docs/python/refdocs/google.appengine.api.urlfetch
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




    @endpoints.method(ID,MensajeRespuesta,path='delAlumno', http_method='DELETE', name='alumnos.delAlumno')
    def eliminar_alumno(self, request):
        '''

        delAlumno()  [DELETE con dniAlumno]

        #Ejemplo de borrado de un recurso pasando el dni de un alumno
        Ubuntu> curl -d "id=1" -X DELETE -G localhost:8001/_ah/api/helloworld/v1/alumnos/eliminaralumn
        {
         "message": "OK"
        }

        #Ejemplo de ejecución en el caso de no encontrar el recurso:
        Ubuntu> curl -d "id=1" -X DELETE -G localhost:8001/_ah/api/hellworld/v1/alumnos/eliminaralumno
        {
         "message": "Elemento no encontrado"
        }
        '''

        if v:
            print nombreMicroservicio
            print "Petición DELETE a alumnos.delAlumno"
            print "Contenido de la petición:"
            print str(request)
            print '\n'

        #Conformamos la dirección:
        url = "http://%s/" % modules.get_hostname(module="microservicio1")

        '''
        Parece que urlfetch da problemas a al hora de pasar parámetros (payload) cuando se trata del
        método DELETE.
        Extracto de la doc:
        payload: POST, PUT, or PATCH payload (implies method is not GET, HEAD, or DELETE). this is ignored if the method is not POST, PUT, or PATCH.
        Además no somos los primeros en encontrarse este problema:
        http://grokbase.com/t/gg/google-appengine/13bvr5qjyq/is-there-any-reason-that-urlfetch-delete-method-does-not-support-a-payload

        Por eso en lugar de pasar los datos por payload los añadimos a la url, que es algo equivalente.

        '''
        #Extraemos el argumento id de la petición y la añadimos a la URL
        url+='alumnos/'+request.id

        if v:
            print "Llamando a: "+url

        #Realizamos la petición a la url del servicio con el método apropiado.
        result = urlfetch.fetch(url=url, method=urlfetch.DELETE)

        #Infro después de la petición:
        if v:
            print nombreMicroservicio
            print "Resultado de la petición: "
            print result.content
            print "Código de estado: "
            print result.status_code


        #Mandamos la respuesta que nos devuelve la llamada al microservicio:
        return MensajeRespuesta(message=result.content)

    @endpoints.method(AlumnoCompleto,MensajeRespuesta,path='alumnos/modAlumnoCompleto', http_method='POST', name='alumnos.modAlumnoCompleto')
    def modificarAlumnoCompleto(self, request):
        '''

        modificarAlumnoCompleto()  [POST]

        Modifica todos los atributos de un alumno, aunque algunos queden igual.

        curl -d "id=1&nombre=Pedro&apellidos=Torrssr&dni=23&direccion=CREalCartuja&localidad=Granada&provincia=Granada&fecha_nacimiento=1988-12-4&telefono=23287282" -i -X POST -G localhost:8001/_ah/api/helloworld/v1/alumnos/modAlumnoCompleto
        HTTP/1.1 200 OK
        content-type: application/json
        Cache-Control: no-cache
        Expires: Fri, 01 Jan 1990 00:00:00 GMT
        Server: Development/2.0
        Content-Length: 20
        Server: Development/2.0
        Date: Mon, 14 Mar 2016 10:17:12 GMT

        {
         "message": "OK"
        }


        '''

        if v:
            print nombreMicroservicio
            print "Petición POST a alumnos.modAlumnoCompleto"
            print "Contenido de la petición:"
            print str(request)
            print '\n'

        if request.nombre==None or request.apellidos==None or request.dni==None or request.direccion==None or request.localidad==None or request.provincia==None or request.fecha_nacimiento==None or request.telefono==None:
            raise endpoints.BadRequestException('Peticion erronea, faltan datos.')

        url = "http://%s/" % modules.get_hostname(module="microservicio1")

        #Añadimos el recurso al que queremos conectarnos, colección alumnos / alumno con id concreto.
        url+="alumnos/"+request.id

        #Extraemos lo datos de la petición que se reciben aquí en el endpoints
        form_fields = {
          "nombre": formatTextInput(request.nombre),
          "apellidos": formatTextInput(request.apellidos),
          "dni": formatTextInput(request.dni),
          "direccion": formatTextInput(request.direccion),
          "localidad": formatTextInput(request.localidad),
          "provincia": formatTextInput(request.provincia),
          "fecha_nacimiento": request.fecha_nacimiento,
          "telefono": request.telefono
        }

        if v:
            print "Llamando a: "+url

        form_data = urllib.urlencode(form_fields)
        result = urlfetch.fetch(url=url, payload=form_data, method=urlfetch.POST)


        #Infro después de la petición:
        if v:
            print nombreMicroservicio
            print "Resultado de la petición: "
            print result.content
            print "Código de estado: "
            print result.status_code

        #return MensajeRespuesta(message="Todo OK man!")
        #Mandamos la respuesta que nos devuelve la llamada al microservicio:
        return MensajeRespuesta(message=result.content)

    # Métodos de información sobre relaciones con otras entidades

    @endpoints.method(ID, ListaProfesores, path='alumnos/getProfesoresAlumno', http_method='GET', name='alumnos.getProfesoresAlumno')
    def getProfesoresAlumno(self, request):
        '''
        Devuelve una lista con los datos completos de los profesores que dan clase al alumno de dni pasado
        curl -i -X GET localhost:8001/_ah/api/helloworld/v1/alumnos/getProfesoresAlumno?id=1
        '''
        #Transformación de la llamada al endpoints a la llamada a la api rest del servicio.
        if v:
            print ("Ejecución de getProfesoresAlumno en apigateway")

        #Conexión a un microservicio específico:

        module = modules.get_current_module_name()
        instance = modules.get_current_instance_id()
        #Le decimos a que microservicio queremos conectarnos (solo usando el nombre del mismo), GAE descubre su URL solo.
        url = "http://%s/" % modules.get_hostname(module="microservicio1")

        #Añadimos a la url la coleccion (alumnos), el recurso (alumno dado por su dni) y el recurso anidado de este (profesores)
        url+='alumnos/'+str(request.id)+"/profesores"


        print url

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
            profesoresItems.append(Profesor( nombre=formatText(profesor.get('nombre')), apellidos=formatText(profesor.get('apellidos')), id=str(profesor.get('id'))))

        #Los adaptamos al tipo de mensaje y enviamos
        #return Greeting(message=str(result.content))
        return ListaProfesores(profesores=profesoresItems)

    @endpoints.method(ID, ListaAsignaturas, path='alumnos/getAsignaturasAlumno', http_method='GET', name='alumnos.getAsignaturasAlumno')
    def getAsignaturasAlumno(self, request):
        '''
        Devuelve una lista con los datos completos de las asignatuas en las que está matriculado el alumno con dni pasado.
        Ejemplo de llamada:
        curl -i -X GET localhost:8001/_ah/api/helloworld/v1/alumnos/getAsignaturasAlumno?id=1
        '''
        if v:
            print ("Ejecución de getAsignaturasAlumno en apigateway")
        module = modules.get_current_module_name()
        instance = modules.get_current_instance_id()
        url = "http://%s/" % modules.get_hostname(module="microservicio1")
        url+='alumnos/'+request.id+"/asignaturas"
        result = urlfetch.fetch(url)
        if v:
            print result.content
        listaAsignaturas = jsonpickle.decode(result.content)
        print listaAsignaturas
        asignaturasItems= []
        for asignatura in listaAsignaturas:
            asignaturasItems.append( Asignatura( id=str(asignatura.get('id')), nombre=formatText(asignatura.get('nombre')) ) )
        return ListaAsignaturas(asignaturas=asignaturasItems)

    @endpoints.method(ID, ListaClases, path='alumnos/getClasesAlumno', http_method='GET', name='alumnos.getClasesAlumno')
    def getClasesAlumno(self, request):
        '''
        Devuelve una lista con los datos completos de las clases en las que está matriculado el alumno con dni pasado.
        Ejemplo de llamada:
        curl -i -X GET localhost:8001/_ah/api/helloworld/v1/alumnos/getClasesAlumno?id=1
        '''
        if v:
            print ("Ejecución de getCursosAlumno en apigateway")
        module = modules.get_current_module_name()
        instance = modules.get_current_instance_id()
        url = "http://%s/" % modules.get_hostname(module="microservicio1")
        url+='alumnos/'+request.id+"/clases"
        result = urlfetch.fetch(url)
        if v:
            print result.content
        listaClases = jsonpickle.decode(result.content)
        print listaClases
        clasesItems= []
        for clase in listaClases:
            clasesItems.append(Clase(id=str(clase.get('id')),curso=str(clase.get('curso')),grupo=str(clase.get('grupo')),nivel=str(clase.get('nivel'))))
        return ListaClases(clases=clasesItems)


    ##############################################
    #   métodos de PROFESORES                    #
    ##############################################

    @endpoints.method(message_types.VoidMessage, ListaProfesores, path='profesores/getProfesores', http_method='GET', name='profesores.getProfesores')
    def getProfesores(self, unused_request):
        '''
        Devuelve una lista con todos los profesores registrados en el sistema, de forma simplificada (solo nombre y ID)

        Llamada desde terminal:
        curl -X GET localhost:8001/_ah/api/helloworld/v1/profesores/getProfesores
        Llamada desde JavaScript:
        response =service.profesores.getProfesores().execute()
        '''
        #Identificación del módulo en el que estamos.
        module = modules.get_current_module_name()
        instance = modules.get_current_instance_id()

        #Leclear decimos a que microservicio queremos conectarnos (solo usando el nombre del mismo), GAE descubre su URL solo.
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
        for profesor in listaProfesores:
            profesoresItems.append(Profesor( nombre=str(profesor.get('nombre')), apellidos=str(profesor.get('apellidos')), id=str(profesor.get('id'))  ))

        #Los adaptamos al tipo de mensaje y enviamos
        #return Greeting(message=str(result.content))
        return ListaProfesores(profesores=profesoresItems)

    @endpoints.method(ID, ProfesorCompleto, path='profesores/getProfesor', http_method='GET', name='profesores.getProfesor')
    def getProfesor(self,request):
        '''
        Devuelve toda la información de un profesor en caso de estar en el sistema.

        Llamada ejemplo desde terminal:
        curl -X GET localhost:8001/_ah/api/helloworld/v1/profesores/getProfesor?id=1
        '''

        #Info de seguimiento
        if v:
            print nombreMicroservicio
            print "Petición GET a profesores.getProfesor"
            print "request: "+str(request)
            print '\n'

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
        url+='profesores/'+request.id

        if v:
            print "Llamando a: "+str(url)

        #Petición al microservicio
        result = urlfetch.fetch(url=url, method=urlfetch.GET)

        print "RESULTADO:"+str(result.status_code)
        #print result.content
        if v:
            print result.status_code
        if str(result.status_code) == '400':
            raise endpoints.BadRequestException('Peticion erronea')

        if str(result.status_code) == '404':
            raise endpoints.NotFoundException('Profesor con ID %s no encontrado.' % (request.id))

        profesor = jsonpickle.decode(result.content)

        #Infro después de la petición:
        if v:
            print nombreMicroservicio
            print "Resultado de la petición: "
            print result.content
            print "\nCódigo de estado: "+str(result.status_code)+'\n'


        #Componemos un mensaje de tipo AlumnoCompleto.
        #Las partes que son enteros las pasamos a string para enviarlos como mensajes de tipo string.
        #Los campos que tengan NULL en la bd no se pasan al tipo message y ese campo queda vaćio y no se muestra.
        profesor = ProfesorCompleto(id=str(profesor.get('id')),
                                nombre=profesor.get('nombre'),
                                apellidos=profesor.get('apellidos'),
                                dni=str(profesor.get('dni')),
                                direccion=profesor.get('direccion'),
                                localidad=profesor.get('localidad'),
                                provincia=profesor.get('provincia'),
                                fecha_nacimiento=str(profesor.get('fecha_nacimiento')),
                                telefono=str(profesor.get('telefono'))
                                )

        return profesor

    @endpoints.method(ProfesorCompleto,MensajeRespuesta, path='profesores/insertarProfesor', http_method='POST', name='profesores.insertarProfesor')
    def insertarProfesor(self, request):
        '''
        Introduce un nuevo profesor en el sistema.

        Ejemplo de llamada en terminal:
        curl -i -d "nombre=Juan&apellidos=Azustregui&dni=99&direccion=Calle&localidad=Jerezfrontera&provincia=Granada&fecha_nacimiento=1988-2-6&telefono=699164459" -X POST -G localhost:8001/_ah/api/helloworld/v1/profesores/insertarProfesor
        (-i para ver las cabeceras)

        '''

        if v:
            print nombreMicroservicio
            print "Petición POST a profesores.insertarProfesor"
            print "Contenido de la petición:"
            print str(request)
            print '\n'

        #Si no tenemos todos los atributos entonces enviamos un error de bad request.
        if request.nombre==None or request.apellidos==None or request.dni==None or request.direccion==None or request.localidad==None or request.provincia==None or request.fecha_nacimiento==None or request.telefono==None:
            raise endpoints.BadRequestException('Peticion erronea, faltan datos.')

        #Conformamos la dirección:
        url = "http://%s/" % modules.get_hostname(module="microservicio1")
        #Añadimos el servicio al que queremos conectarnos.
        url+="profesores"


        #Extraemos lo datos de la petición al endpoints
        form_fields = {
          "nombre": request.nombre,
          "apellidos": request.apellidos,
          "dni": request.dni,
          "direccion": request.direccion,
          "localidad": request.localidad,
          "provincia": request.provincia,
          "fecha_nacimiento": request.fecha_nacimiento,
          "telefono": request.telefono
        }

        if v:
            print "Llamando a: "+url


        ##Doc de urlfetch: https://cloud.google.com/appengine/docs/python/refdocs/google.appengine.api.urlfetch
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

    @endpoints.method(ID,MensajeRespuesta,path='profesores/delProfesor', http_method='DELETE', name='profesores.delProfesor')
    def delProfesor(self, request):

        '''
        delProfesor()

        #Ejemplo de borrado de un recurso pasando el id de un profesor
        Ubuntu> curl -d "dni=1" -X DELETE -G localhost:8001/_ah/api/helloworld/v1/profesores/delProfesor
        {
         "message": "OK"
        }

        #Ejemplo de ejecución en el caso de no encontrar el recurso:
        Ubuntu> curl -d "dni=1" -X DELETE -G localhost:8001/_ah/api/hellworld/v1/profesor/delProfesor
        {
         "message": "Elemento no encontrado"
        }
        '''

        if v:
            print nombreMicroservicio
            print "Petición al método profesores.delProfesor de APIGateway"
            print "Contenido de la petición:"
            print str(request)
            print '\n'

        #Conformamos la dirección:
        url = "http://%s/" % modules.get_hostname(module="microservicio1")


        #Extraemos el argumento id de la petición y la añadimos a la URL
        url+='alumnos/'+request.id

        if v:
            print "Llamando a: "+url

        #Realizamos la petición a la url del servicio con el método apropiado.
        result = urlfetch.fetch(url=url, method=urlfetch.DELETE)

        #Infro después de la petición:
        if v:
            print nombreMicroservicio
            print "Resultado de la petición: "
            print result.content
            print "Código de estado: "
            print result.status_code


        #Mandamos la respuesta que nos devuelve la llamada al microservicio:
        return MensajeRespuesta(message=result.content)

    @endpoints.method(ProfesorCompleto,MensajeRespuesta,path='profesores/modProfesorCompleto', http_method='POST', name='profesores.modProfesorCompleto')
    def modificarProfesorCompleto(self, request):
        '''
        Modifica todos los atributos de un profesor, aunque algunos queden igual.
        curl -d "id=1&nombre=Pedro&apellidos=Torrssr&dni=23&direccion=CREalCartuja&localidad=Granada&provincia=Granada&fecha_nacimiento=1988-12-4&telefono=23287282" -i -X POST -G localhost:8001/_ah/api/helloworld/v1/profesores/modProfesorCompleto
        '''

        if v:
            print nombreMicroservicio
            print "Petición POST a alumnos.modAlumnoCompleto"
            print "Contenido de la petición:"
            print str(request)
            print '\n'

        if request.nombre==None or request.apellidos==None or request.dni==None or request.direccion==None or request.localidad==None or request.provincia==None or request.fecha_nacimiento==None or request.telefono==None:
            raise endpoints.BadRequestException('Peticion erronea, faltan datos.')

        url = "http://%s/" % modules.get_hostname(module="microservicio1")

        #Añadimos el recurso al que queremos conectarnos, colección alumnos / alumno con id concreto.
        url+="profesores/"+request.id

        #Extraemos lo datos de la petición que se reciben aquí en el endpoints
        form_fields = {
          "nombre": request.nombre,
          "apellidos": request.apellidos,
          "dni": request.dni,
          "direccion": request.direccion,
          "localidad": request.localidad,
          "provincia": request.provincia,
          "fecha_nacimiento": request.fecha_nacimiento,
          "telefono": request.telefono
        }

        if v:
            print "Llamando a: "+url

        form_data = urllib.urlencode(form_fields)
        result = urlfetch.fetch(url=url, payload=form_data, method=urlfetch.POST)


        #Infro después de la petición:
        if v:
            print nombreMicroservicio
            print "Resultado de la petición: "
            print result.content
            print "Código de estado: "
            print result.status_code

        #return MensajeRespuesta(message="Todo OK man!")
        #Mandamos la respuesta que nos devuelve la llamada al microservicio:
        return MensajeRespuesta(message=result.content)

    #Métodos de relación con otras entidades.

    @endpoints.method(ID, ListaAlumnos, path='profesores/getAlumnosProfesor', http_method='GET', name='profesores.getAlumnosProfesor')
    def getAlumnosProfesores(self, request):
        '''
        Devuelve una lista con los datos resumidos de los alumnos a los que el profesor con id pasado da clase.
        curl -i -X GET localhost:8001/_ah/api/helloworld/v1/profesores/getAlumnosProfesor?id=1
        '''
        #Transformación de la llamada al endpoints a la llamada a la api rest del servicio.
        if v:
            print ("Ejecución de getAlumnosProfesor en apigateway")

        #Conexión a un microservicio específico:

        module = modules.get_current_module_name()
        instance = modules.get_current_instance_id()
        #Le decimos a que microservicio queremos conectarnos (solo usando el nombre del mismo), GAE descubre su URL solo.
        url = "http://%s/" % modules.get_hostname(module="microservicio1")

        #Añadimos a la url la coleccion (alumnos), el recurso (alumno dado por su dni) y el recurso anidado de este (profesores)
        url+='profesores/'+str(request.id)+"/alumnos"


        print url

        #Realizamos la petición
        result = urlfetch.fetch(url)

        #Vamos a intentar consumir los datos en JSON y convertirlos a un mensje enviable :)

        print "IMPRESION DE LOS DATOS RECIBIDOS"
        print result.content
        listaAlumnos = jsonpickle.decode(result.content)

        #Creamos un vector
        vectorAlumnos= []
        #Que rellenamos con todo los alumnos de la listaAlumnos
        for alumno in listaAlumnos:
            vectorAlumnos.append(Alumno( nombre=formatText(alumno.get('nombre')), apellidos=formatText(alumno.get('apellidos')), id=str(alumno.get('id'))))

        #Los adaptamos al tipo de mensaje y enviamos
        #return Greeting(message=str(result.content))
        return ListaAlumnos(alumnos=vectorAlumnos)

    @endpoints.method(ID, ListaAsignaturas, path='profesores/getAsignaturasProfesor', http_method='GET', name='profesores.getAsignaturasProfesor')
    def getAsignaturasProfesor(self, request):
        '''
        Devuelve una lista con los datos completos de las asignatuas que el profesor en cuestión imparte.
        Ejemplo de llamada:
        curl -i -X GET localhost:8001/_ah/api/helloworld/v1/profesores/getAsignaturasProfesor?id=1
        '''
        if v:
            print ("Ejecución de getAsignaturasProfesor en apigateway")
        module = modules.get_current_module_name()
        instance = modules.get_current_instance_id()
        url = "http://%s/" % modules.get_hostname(module="microservicio1")
        url+='profesores/'+request.id+"/asignaturas"
        result = urlfetch.fetch(url)
        if v:
            print result.content
        listaAsignaturas = jsonpickle.decode(result.content)
        print listaAsignaturas
        asignaturasItems= []

        for asignatura in listaAsignaturas:
            asignaturasItems.append( Asignatura( id=str(asignatura.get('id')), nombre=formatText(asignatura.get('nombre')) ) )
        return ListaAsignaturas(asignaturas=asignaturasItems)

    @endpoints.method(ID, ListaClases, path='profesores/getClasesProfesor', http_method='GET', name='profesores.getClasesProfesor')
    def getClasesProfesor(self, request):
        '''
        Devuelve una lista con los datos minimos de las clases a las que ese profesor imparte.
        Ejemplo de llamada:
        curl -i -X GET localhost:8001/_ah/api/helloworld/v1/profesores/getClasesProfesor?id=1
        '''
        if v:
            print ("Ejecución de getClasesProfesor en apigateway")
        module = modules.get_current_module_name()
        instance = modules.get_current_instance_id()
        url = "http://%s/" % modules.get_hostname(module="microservicio1")
        url+='profesores/'+request.id+"/clases"
        result = urlfetch.fetch(url)
        if v:
            print result.content
        listaClases = jsonpickle.decode(result.content)
        print listaClases
        clasesItems= []
        for clase in listaClases:
            clasesItems.append(Clase(id=str(clase.get('id')),curso=str(clase.get('curso')),grupo=str(clase.get('grupo')),nivel=str(clase.get('nivel'))))
        return ListaClases(clases=clasesItems)


    ##############################################
    #   métodos de ASIGNATURAS                   #
    ##############################################

    @endpoints.method(message_types.VoidMessage, ListaAsignaturas, path='asignaturas/getAsignaturas', http_method='GET', name='asignaturas.getAsignaturas')
    def getAsignaturas(self, unused_request):
        '''
        Devuelve una lista con todos las asignaturas registrados en el sistema, de forma simplificada (solo nombre y ID)

        Llamada desde terminal:
        curl -X GET localhost:8001/_ah/api/helloworld/v1/asignaturas/getAsignaturas
        Llamada desde JavaScript:
        response = service.asignaturas.getAsignaturas().execute()
        '''
        #Identificación del módulo en el que estamos.
        module = modules.get_current_module_name()
        instance = modules.get_current_instance_id()

        #Leclear decimos a que microservicio queremos conectarnos (solo usando el nombre del mismo), GAE descubre su URL solo.
        url = "http://%s/" % modules.get_hostname(module="microservicio1")
        #Añadimos el recurso al que queremos conectarnos.
        url+="asignaturas"
        if v:
            print str(url)
        #Al no especificar nada se llama al método GET de la URL.
        result = urlfetch.fetch(url)
        if v:
            print result.content
        listaAsignaturas = jsonpickle.decode(result.content)

        #Creamos un vector
        asignaturasItems= []
        #Que rellenamos con todo los asignaturas de la listaProfesores
        for asignatura in listaAsignaturas:
            asignaturasItems.append(Asignatura( id=str(asignatura.get('id')), nombre=formatText(asignatura.get('nombre')) ))

        #Los adaptamos al tipo de mensaje y enviamos
        #return Greeting(message=str(result.content))
        return ListaAsignaturas(asignaturas=asignaturasItems)

    @endpoints.method(ID, AsignaturaCompleta, path='asignaturas/getAsignatura', http_method='GET', name='asignaturas.getAsignatura')
    def getAsignatura(self,request):
        '''
        Devuelve toda la información de un profesor en caso de estar en el sistema.

        Llamada ejemplo desde terminal:
        curl -X GET localhost:8001/_ah/api/helloworld/v1/asignaturas/getAsignatura?id=1
        '''

        #Info de seguimiento
        if v:
            print nombreMicroservicio
            print "Petición GET a asignaturas.getAsignatura"
            print "request: "+str(request)
            print '\n'

        #Conexión a un microservicio específico:
        module = modules.get_current_module_name()
        instance = modules.get_current_instance_id()

        #Le decimos al microservicio que queremos conectarnos (solo usando el nombre del mismo), GAE descubre su URL solo.
        url = "http://%s/" % modules.get_hostname(module="microservicio1")

        #Recursos más entidad
        url+='asignaturas/'+request.id

        if v:
            print "Llamando a: "+str(url)

        #Petición al microservicio
        result = urlfetch.fetch(url=url, method=urlfetch.GET)

        print "RESULTADO:"+str(result.status_code)
        #print result.content
        if v:
            print result.status_code
        if str(result.status_code) == '400':
            raise endpoints.BadRequestException('Peticion erronea')

        if str(result.status_code) == '404':
            raise endpoints.NotFoundException('Profesor con ID %s no encontrado.' % (request.id))

        profesor = jsonpickle.decode(result.content)

        #Infro después de la petición:
        if v:
            print nombreMicroservicio
            print "Resultado de la petición: "
            print result.content
            print "\nCódigo de estado: "+str(result.status_code)+'\n'


        #Componemos un mensaje de tipo AlumnoCompleto.
        #Las partes que son enteros las pasamos a string para enviarlos como mensajes de tipo string.
        #Los campos que tengan NULL en la bd no se pasan al tipo message y ese campo queda vaćio y no se muestra.
        asignatura = AsignaturaCompleta(id=str(profesor.get('id')),
                                nombre=profesor.get('nombre')
                                )

        return asignatura

    @endpoints.method(AsignaturaCompleta, MensajeRespuesta, path='asignaturas/insertarAsignatura', http_method='POST', name='asignaturas.insertarAsignatura')
    def insertarAsignatura(self, request):
        '''
        Introduce un nuevo profesor en el sistema.

        Ejemplo de llamada en terminal:
        curl -i -d "nombre=CienciasExperimentales" -X POST -G localhost:8001/_ah/api/helloworld/v1/asignaturas/insertarAsignatura
        '''

        if v:
            print nombreMicroservicio
            print "Petición POST a asignaturas.insertarAsignatura"
            print "Contenido de la petición:"
            print str(request)
            print '\n'

        #Si no tenemos todos los atributos entonces enviamos un error de bad request.
        if request.nombre==None:
            raise endpoints.BadRequestException('Peticion erronea, faltan datos.')

        #Conformamos la dirección:
        url = "http://%s/" % modules.get_hostname(module="microservicio1")
        #Añadimos el servicio al que queremos conectarnos.
        url+="asignaturas"


        #Extraemos lo datos de la petición al endpoints
        form_fields = {
          "nombre": formatTextInput(request.nombre)
        }
        if v:
            print 'form_fields:'
            print form_fields
            print "Llamando a: "+url


        ##Doc de urlfetch: https://cloud.google.com/appengine/docs/python/refdocs/google.appengine.api.urlfetch
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

        return MensajeRespuesta(message=result.content)

    @endpoints.method(ID,MensajeRespuesta,path='asignaturas/delAsignatura', http_method='DELETE', name='asignaturas.delAsignatura')
    def delAsignatura(self, request):

        '''
        delProfesor()

        #Ejemplo de borrado de un recurso pasando el id de un profesor
        Ubuntu> curl -d "id=1" -X DELETE -G localhost:8001/_ah/api/helloworld/v1/asignaturas/delAsignatura
        {
         "message": "OK"
        }

        #Ejemplo de ejecución en el caso de no encontrar el recurso:
        Ubuntu> curl -d "dni=1" -X DELETE -G localhost:8001/_ah/api/hellworld/v1/asignaturas/delAsignatura
        {
         "message": "Elemento no encontrado"
        }
        '''

        if v:
            print nombreMicroservicio
            print "Petición al método asignaturas.delAsignatura de APIGateway"
            print "Contenido de la petición:"
            print str(request)
            print '\n'

        #Conformamos la dirección:
        url = "http://%s/" % modules.get_hostname(module="microservicio1")


        #Extraemos el argumento id de la petición y la añadimos a la URL
        url+='asignaturas/'+request.id

        if v:
            print "Llamando a: "+url

        #Realizamos la petición a la url del servicio con el método apropiado DELETE
        result = urlfetch.fetch(url=url, method=urlfetch.DELETE)

        #Infro después de la petición:
        if v:
            print nombreMicroservicio
            print "Resultado de la petición: "
            print result.content
            print "Código de estado: "
            print result.status_code


        #Mandamos la respuesta que nos devuelve la llamada al microservicio:
        return MensajeRespuesta(message=result.content)

    @endpoints.method(AsignaturaCompleta,MensajeRespuesta,path='asignaturas/modAsignaturaCompleta', http_method='POST', name='asignaturas.modAsignaturaCompleta')
    def modificarAsignaturaCompleta(self, request):
        '''
        Modifica todos los atributos de una asignatura, aunque algunos queden igual.
        curl -d "id=1&nombre=Chinorri" -i -X POST -G localhost:8001/_ah/api/helloworld/v1/asignaturas/modAsignaturaCompleta
        '''

        if v:
            print nombreMicroservicio
            print "Petición POST a asignaturas.modAsignaturaCompleta"
            print "Contenido de la petición:"
            print str(request)
            print '\n'

        if request.nombre==None or request.id==None:
            raise endpoints.BadRequestException('Peticion erronea, faltan datos.')

        url = "http://%s/" % modules.get_hostname(module="microservicio1")

        #Añadimos el recurso al que queremos conectarnos, colección alumnos / alumno con id concreto.
        url+="asignaturas/"+request.id

        #Extraemos lo datos de la petición que se reciben aquí en el endpoints
        form_fields = {
          "nombre": formatTextInput(request.nombre)
        }

        if v:
            print "Llamando a: "+url

        form_data = urllib.urlencode(form_fields)
        result = urlfetch.fetch(url=url, payload=form_data, method=urlfetch.POST)


        #Infro después de la petición:
        if v:
            print nombreMicroservicio
            print "Resultado de la petición: "
            print result.content
            print "Código de estado: "
            print result.status_code

        return MensajeRespuesta(message=result.content)

    #Métodos de relaciones con otras entidades

    @endpoints.method(ID, ListaAlumnos, path='asignaturas/getAlumnosAsignatura', http_method='GET', name='asignaturas.getAlumnosAsignatura')
    def getAlumnosAsignatura(self, request):
        '''
        Devuelve una lista con los datos resumidos de los alumnos que esta matriculados en esa clase
        curl -i -X GET localhost:8001/_ah/api/helloworld/v1/asignaturas/getAlumnosAsignatura?id=1
        '''
        #Transformación de la llamada al endpoints a la llamada a la api rest del servicio.
        if v:
            print ("Ejecución de getAlumnosAsignatura en apigateway")

        #Conexión a un microservicio específico:

        module = modules.get_current_module_name()
        instance = modules.get_current_instance_id()
        #Le decimos a que microservicio queremos conectarnos (solo usando el nombre del mismo), GAE descubre su URL solo.
        url = "http://%s/" % modules.get_hostname(module="microservicio1")

        #Añadimos a la url la coleccion (alumnos), el recurso (alumno dado por su dni) y el recurso anidado de este (profesores)
        url+='asignaturas/'+str(request.id)+"/alumnos"


        print url

        #Realizamos la petición
        result = urlfetch.fetch(url)

        #Vamos a intentar consumir los datos en JSON y convertirlos a un mensje enviable :)

        print "IMPRESION DE LOS DATOS RECIBIDOS"
        print result.content
        listaAlumnos = jsonpickle.decode(result.content)

        #Creamos un vector
        vectorAlumnos= []
        #Que rellenamos con todo los alumnos de la listaAlumnos
        for alumno in listaAlumnos:
            vectorAlumnos.append(Alumno( nombre=formatText(alumno.get('nombre')),
                                         apellidos=formatText(alumno.get('apellidos')),
                                         id=str(alumno.get('id'))
                                         )
                                )

        #Los adaptamos al tipo de mensaje y enviamos
        #return Greeting(message=str(result.content))
        return ListaAlumnos(alumnos=vectorAlumnos)

    @endpoints.method(ID, ListaProfesores, path='asignaturas/getProfesoresAsignatura', http_method='GET', name='asignaturas.getProfesoresAsignatura')
    def getProfesoresAsignatura(self, request):
        '''
        Devuelve una lista con los datos simplificados de los profesores que imparten clase en una asignatura.
        Ejemplo de llamada:
        > curl -i -X GET localhost:8001/_ah/api/helloworld/v1/asignaturas/getProfesoresAsignatura?id=1
        '''
        if v:
            print ("Ejecución de getProfesoresAsignatura en apigateway")
        module = modules.get_current_module_name()
        instance = modules.get_current_instance_id()
        url = "http://%s/" % modules.get_hostname(module="microservicio1")
        url+='asignaturas/'+request.id+"/profesores"
        result = urlfetch.fetch(url)
        if v:
            print result.content
        listaProfesores = jsonpickle.decode(result.content)
        print listaProfesores
        profesoresItems= []
        for profesor in listaProfesores:
            profesoresItems.append( Profesor( id=str(profesor.get('id')), nombre=str(profesor.get('nombre')), apellidos=str(profesor.get('apellidos')) ) )
        return ListaProfesores(profesores=profesoresItems)

    @endpoints.method(ID, ListaClases, path='asignaturas/getClasesAsignatura', http_method='GET', name='asignaturas.getClasesAsignatura')
    def getClasesAsignatura(self, request):
        '''
        Devuelve una lista con los datos minimos de las clases en las que se imparte esa asignatura
        Ejemplo de llamada:
        > curl -i -X GET localhost:8001/_ah/api/helloworld/v1/asignaturas/getClasesAsignatura?id=1
        '''
        if v:
            print ("Ejecución de getClasesProfesor en apigateway")
        module = modules.get_current_module_name()
        instance = modules.get_current_instance_id()
        url = "http://%s/" % modules.get_hostname(module="microservicio1")
        url+='asignaturas/'+request.id+"/clases"
        result = urlfetch.fetch(url)
        if v:
            print url
            print "Respuesta del microservicio: \n"
            print result.content
            print "\n"
        listaClases = jsonpickle.decode(result.content)
        print listaClases
        clasesItems= []
        for clase in listaClases:
            clasesItems.append(Clase(id=str(clase.get('id')),curso=str(clase.get('curso')),grupo=str(clase.get('grupo')),nivel=str(clase.get('nivel'))))
        return ListaClases(clases=clasesItems)


    ##############################################
    #   métodos de CLASES                        #
    ##############################################

    @endpoints.method(message_types.VoidMessage, ListaClases, path='clases/getClases', http_method='GET', name='clases.getClases')
    def getClases(self, unused_request):
        '''
        Devuelve una lista con todos las clases registrados en el sistema, de forma simplificada, id_clase, curso, grupo y nivel

        Llamada desde terminal:
        curl -X GET localhost:8001/_ah/api/helloworld/v1/clases/getClases
        Llamada desde JavaScript:
        response = service.clases.getClases().execute()
        '''
        #Identificación del módulo en el que estamos.
        module = modules.get_current_module_name()
        instance = modules.get_current_instance_id()

        #Leclear decimos a que microservicio queremos conectarnos (solo usando el nombre del mismo), GAE descubre su URL solo.
        url = "http://%s/" % modules.get_hostname(module="microservicio1")
        #Añadimos el recurso al que queremos conectarnos.
        url+="clases"
        if v:
            print str(url)
        #Al no especificar nada se llama al método GET de la URL.
        result = urlfetch.fetch(url)
        if v:
            print result.content
        listaClases = jsonpickle.decode(result.content)

        #Creamos un vector
        clasesItems= []
        #Que rellenamos con todo los asignaturas de la listaProfesores
        for clase in listaClases:
            clasesItems.append(Clase( id=str(clase.get('id')), curso=str(clase.get('curso')), grupo=str(clase.get('grupo')), nivel=str(clase.get('nivel')) ))

        return ListaClases(clases=clasesItems)

    @endpoints.method(ID, ClaseCompleta, path='clases/getClase', http_method='GET', name='clases.getClase')
    def getClase(self,request):
        '''
        Devuelve toda la información de una clase en caso de estar en el sistema.

        Llamada ejemplo desde terminal:
        curl -X GET localhost:8001/_ah/api/helloworld/v1/clases/getClase?id=1
        '''

        #Info de seguimiento
        if v:
            print nombreMicroservicio
            print "Petición GET a clases.getClase"
            print "request: "+str(request)
            print '\n'

        #Conexión a un microservicio específico:
        module = modules.get_current_module_name()
        instance = modules.get_current_instance_id()

        #Le decimos al microservicio que queremos conectarnos (solo usando el nombre del mismo), GAE descubre su URL solo.
        url = "http://%s/" % modules.get_hostname(module="microservicio1")

        #Recursos más entidad
        url+='clases/'+request.id

        if v:
            print "Llamando a: "+str(url)

        #Petición al microservicio
        result = urlfetch.fetch(url=url, method=urlfetch.GET)

        print "RESULTADO:"+str(result.status_code)
        #print result.content
        if v:
            print result.status_code
        if str(result.status_code) == '400':
            raise endpoints.BadRequestException('Peticion erronea')

        if str(result.status_code) == '404':
            raise endpoints.NotFoundException('Profesor con ID %s no encontrado.' % (request.id))

        clase = jsonpickle.decode(result.content)

        #Infro después de la petición:
        if v:
            print nombreMicroservicio
            print "Resultado de la petición: "
            print result.content
            print "\nCódigo de estado: "+str(result.status_code)+'\n'


        #Componemos un mensaje de tipo AlumnoCompleto.
        #Las partes que son enteros las pasamos a string para enviarlos como mensajes de tipo string.
        #Los campos que tengan NULL en la bd no se pasan al tipo message y ese campo queda vaćio y no se muestra.
        clase = ClaseCompleta(id=str(clase.get('id')), curso=str(clase.get('curso')), grupo=str(clase.get('grupo')), nivel=str(clase.get('nivel')) )


        return clase

    @endpoints.method(ClaseCompleta, MensajeRespuesta, path='clases/insertarClase', http_method='POST', name='clases.insertarClase')
    def insertarClase(self, request):
        '''
        Introduce una nueva clase en el sistema.

        Ejemplo de llamada en terminal:
        curl -i -d "curso=4&grupo=B&nivel=Primaria" -X POST -G localhost:8001/_ah/api/helloworld/v1/clases/insertarClase
        '''

        if v:
            print nombreMicroservicio
            print "Petición POST a clases.insertarClase"
            print "Contenido de la petición:"
            print str(request)
            print '\n'

        #Si no tenemos todos los atributos entonces enviamos un error de bad request.
        if request.curso==None or request.grupo==None or request.nivel==None:
            raise endpoints.BadRequestException('Peticion erronea, faltan datos.')

        #Conformamos la dirección:
        url = "http://%s/" % modules.get_hostname(module="microservicio1")
        #Añadimos el servicio al que queremos conectarnos.
        url+="clases"


        #Extraemos lo datos de la petición al endpoints
        form_fields = {
          "curso": request.curso,
          "grupo": request.grupo,
          "nivel": request.nivel,
        }

        if v:
            print "Llamando a: "+url


        ##Doc de urlfetch: https://cloud.google.com/appengine/docs/python/refdocs/google.appengine.api.urlfetch
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

        return MensajeRespuesta(message=result.content)

    @endpoints.method(ID,MensajeRespuesta,path='clases/delClase', http_method='DELETE', name='clases.delClase')
    def delClase(self, request):

        '''
        Elimina la clase con id pasado en caso de existir en el sistema.

        #Ejemplo de borrado de un recurso pasando el id de la clase.
        Ubuntu> curl -d "id=1" -X DELETE -G localhost:8001/_ah/api/helloworld/v1/clases/delClase
        {
         "message": "OK"
        }
        '''

        if v:
            print nombreMicroservicio
            print "Petición al método clases.delClase de APIGateway"
            print "Contenido de la petición:"
            print str(request)
            print '\n'

        #Conformamos la dirección:
        url = "http://%s/" % modules.get_hostname(module="microservicio1")


        #Extraemos el argumento id de la petición y la añadimos a la URL
        url+='clases/'+request.id

        if v:
            print "Llamando a: "+url

        #Realizamos la petición a la url del servicio con el método apropiado DELETE
        result = urlfetch.fetch(url=url, method=urlfetch.DELETE)

        #Infro después de la petición:
        if v:
            print nombreMicroservicio
            print "Resultado de la petición: "
            print result.content
            print "Código de estado: "
            print result.status_code


        #Mandamos la respuesta que nos devuelve la llamada al microservicio:
        return MensajeRespuesta(message=result.content)

    @endpoints.method(ClaseCompleta,MensajeRespuesta,path='clases/modClaseCompleta', http_method='POST', name='clases.modClaseCompleta')
    def modificarClaseCompleta(self, request):
        '''
        Modifica todos los atributos de una clase, aunque algunos queden igual.
        curl -d "id=1&curso=1&grupo=B&nivel=BACH" -i -X POST -G localhost:8001/_ah/api/helloworld/v1/clases/modClaseCompleta
        '''

        if v:
            print nombreMicroservicio
            print "Petición POST a asignaturas.modAsignaturaCompleta"
            print "Contenido de la petición:"
            print str(request)
            print '\n'

        if  request.id==None or request.curso==None or request.grupo==None or request.nivel==None:
            raise endpoints.BadRequestException('Peticion erronea, faltan datos.')

        url = "http://%s/" % modules.get_hostname(module="microservicio1")

        #Añadimos el recurso al que queremos conectarnos, colección alumnos / alumno con id concreto.
        url+="clases/"+request.id

        #Extraemos lo datos de la petición que se reciben aquí en el endpoints
        form_fields = {
          "curso": request.curso,
          "grupo": request.grupo,
          "nivel": request.nivel
        }

        if v:
            print "Llamando a: "+url

        form_data = urllib.urlencode(form_fields)
        result = urlfetch.fetch(url=url, payload=form_data, method=urlfetch.POST)


        #Infro después de la petición:
        if v:
            print nombreMicroservicio
            print "Resultado de la petición: "
            print result.content
            print "Código de estado: "
            print result.status_code

        return MensajeRespuesta(message=result.content)

    #Métodos de relaciones con otras entidades

    @endpoints.method(ID, ListaAlumnos, path='clases/getAlumnosClase', http_method='GET', name='clases.getAlumnosClase')
    def getAlumnosClase(self, request):
        '''
        Devuelve una lista con los datos resumidos de los alumnos que esta matriculados en esa clase
        curl -i -X GET localhost:8001/_ah/api/helloworld/v1/clases/getAlumnosClase?id=1
        '''
        #Transformación de la llamada al endpoints a la llamada a la api rest del servicio.
        if v:
            print ("Ejecución de getAlumnosClase en apigateway")

        module = modules.get_current_module_name()
        instance = modules.get_current_instance_id()
        url = "http://%s/" % modules.get_hostname(module="microservicio1")
        url+='clases/'+str(request.id)+"/alumnos"

        if v:
            print url

        #Realizamos la petición
        result = urlfetch.fetch(url)

        if v:
            print "IMPRESION DE LOS DATOS RECIBIDOS"
            print result.content
        listaAlumnos = jsonpickle.decode(result.content)
        vectorAlumnos= []
        for alumno in listaAlumnos:
            vectorAlumnos.append(Alumno( id=str(alumno.get('id')), nombre=formatText(alumno.get('nombre')), apellidos=formatText(alumno.get('apellidos'))))
        return ListaAlumnos(alumnos=vectorAlumnos)

    @endpoints.method(ID, ListaProfesores, path='clases/getProfesoresClase', http_method='GET', name='clases.getProfesoresClase')
    def getProfesoresClase(self, request):
        '''
        Devuelve una lista con los datos simplificados de los profesores que imparten alguna asignatura a esa clase.
        Ejemplo de llamada:
        curl -i -X GET localhost:8001/_ah/api/helloworld/v1/clases/getProfesoresClase?id=1
        '''
        if v:
            print ("Ejecución de getProfesoresAsignatura en apigateway")
        module = modules.get_current_module_name()
        instance = modules.get_current_instance_id()
        url = "http://%s/" % modules.get_hostname(module="microservicio1")
        url+='clases/'+request.id+"/profesores"
        result = urlfetch.fetch(url)
        if v:
            print result.content
        listaProfesores = jsonpickle.decode(result.content)
        print listaProfesores
        profesoresItems= []
        for profesor in listaProfesores:
            profesoresItems.append( Profesor( id=str(profesor.get('id')), nombre=formatText(profesor.get('nombre')), apellidos=formatText(profesor.get('apellidos')) ) )
        return ListaProfesores(profesores=profesoresItems)

    @endpoints.method(ID, ListaAsignaturas, path='clases/getAsignaturasClase', http_method='GET', name='clases.getAsignaturasClase')
    def getAsignaturasClase(self, request):
        '''
        Devuelve una lista con los datos mínimos de las asignaturas que se imparten en una clase.
        Ejemplo de llamada:
        > curl -i -X GET localhost:8001/_ah/api/helloworld/v1/clases/getAsignaturasClase?id=1
        '''
        if v:
            print ("Ejecución de getAsignaturasProfesor en apigateway")
        module = modules.get_current_module_name()
        instance = modules.get_current_instance_id()
        url = "http://%s/" % modules.get_hostname(module="microservicio1")
        url+='clases/'+request.id+"/asignaturas"
        result = urlfetch.fetch(url)
        if v:
            print result.content
        listaAsignaturas = jsonpickle.decode(result.content)
        print listaAsignaturas
        asignaturasItems= []
        for asignatura in listaAsignaturas:
            asignaturasItems.append( Asignatura( id=str(asignatura.get('id')), nombre=formatText(asignatura.get('nombre')) ) )
        return ListaAsignaturas(asignaturas=asignaturasItems)

    @endpoints.method(ID, ListaAsociaciones, path='clases/getAsociacionesClase', http_method='GET', name='clases.getAsociacionesClase')
    def getAsociacionesClase(self, request):
        '''
            curl -i -X GET localhost:8001/_ah/api/helloworld/v1/clases/getAsociacionesClase?id=1
        '''
        if v:
            print ("Ejecución de getAsociacionesClase en apigateway")
        module = modules.get_current_module_name()
        instance = modules.get_current_instance_id()
        url = "http://%s/" % modules.get_hostname(module="microservicio1")
        url+='clases/'+request.id+"/asociaciones"
        result = urlfetch.fetch(url)
        if v:
            print result.content
        listaAsociaciones = jsonpickle.decode(result.content)
        print listaAsociaciones
        listaAS= []

        for a in listaAsociaciones:
            listaAS.append( Asociacion( id_asociacion=str(a.get('id')), id_clase=str(a.get('idClase')), id_asignatura=str(a.get('idAsignatura')), nombreAsignatura=formatText(a.get('nombreAsignatura')) ) )
        return ListaAsociaciones(asociaciones=listaAS)

    ##############################################
    #   métodos de MATRICULAS                    #
    ##############################################

    @endpoints.method(message_types.VoidMessage, ListaMatriculas, path='matriculas/getMatriculas', http_method='GET', name='matriculas.getMatriculas')
    def getMatriculas(self, unused_request):
        '''
        Devuelve una lista con todos las matriculas registrados en el sistema.

        Llamada desde terminal:
        curl -X GET localhost:8001/_ah/api/helloworld/v1/matriculas/getMatriculas
        Llamada desde JavaScript:
        response = service.matriculas.getMatriculas().execute()
        '''
        #Identificación del módulo en el que estamos.
        module = modules.get_current_module_name()
        instance = modules.get_current_instance_id()

        #Leclear decimos a que microservicio queremos conectarnos (solo usando el nombre del mismo), GAE descubre su URL solo.
        url = "http://%s/" % modules.get_hostname(module="microservicio1")
        #Añadimos el recurso al que queremos conectarnos.
        url+="matriculas"
        if v:
            print str(url)
        #Al no especificar nada se llama al método GET de la URL.
        result = urlfetch.fetch(url)
        if v:
            print result.content
        listaMatriculas = jsonpickle.decode(result.content)

        #Creamos un vector
        matriculasItems= []

        for matricula in listaMatriculas:
            matriculasItems.append(Matricula( id_matricula=str(matricula.get('id')),
                                              id_alumno=str(matricula.get('id_alumno')),
                                              id_asociacion=str(matricula.get('id_asociacion'))
                                            ))

        return ListaMatriculas(matriculas=matriculasItems)

    @endpoints.method(Matricula, MensajeRespuesta, path='matriculas/insertarMatricula', http_method='POST', name='matriculas.insertarMatricula')
    def insertarMatricula(self, request):
        '''
        Introduce una nueva clase en el sistema.

        Ejemplo de llamada en terminal:
        curl -i -d "id_alumno=2&id_asociacion=2" -X POST -G localhost:8001/_ah/api/helloworld/v1/matriculas/insertarMatricula
        '''

        if v:
            print nombreMicroservicio
            print "Petición POST a clases.insertarClase"
            print "Contenido de la petición:"
            print str(request)
            print '\n'

        #Si no tenemos todos los atributos entonces enviamos un error de bad request.
        if request.id_alumno==None or request.id_asociacion==None:
            raise endpoints.BadRequestException('Peticion erronea, faltan datos.')

        #Conformamos la dirección:
        url = "http://%s/" % modules.get_hostname(module="microservicio1")
        #Añadimos el servicio al que queremos conectarnos.
        url+="matriculas"


        #Extraemos lo datos de la petición al endpoints
        form_fields = {
          "id_alumno": request.id_alumno,
          "id_asociacion": request.id_asociacion
        }

        if v:
            print "Llamando a: "+url


        ##Doc de urlfetch: https://cloud.google.com/appengine/docs/python/refdocs/google.appengine.api.urlfetch
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

        return MensajeRespuesta(message=result.content)

    @endpoints.method(ID,MensajeRespuesta,path='matriculas/delMatricula', http_method='DELETE', name='matriculas.delMatricula')
    def delMatricula(self, request):

        '''
        Elimina una matriculación en el sistema, identificándola con su id.

        #Ejemplo de borrado de una matrícula:
        curl -d "id=2" -X DELETE -G localhost:8001/_ah/api/helloworld/v1/matriculas/delMatricula
        {
         "message": "OK"
        }
        '''

        if v:
            print nombreMicroservicio
            print "Petición al método clases.delClase de APIGateway"
            print "Contenido de la petición:"
            print str(request)
            print '\n'

        #Conformamos la dirección:
        url = "http://%s/" % modules.get_hostname(module="microservicio1")


        #Extraemos el argumento id de la petición y la añadimos a la URL
        url+='matriculas/'+request.id

        if v:
            print "Llamando a: "+url

        #Realizamos la petición a la url del servicio con el método apropiado DELETE
        result = urlfetch.fetch(url=url, method=urlfetch.DELETE)

        #Infro después de la petición:
        if v:
            print nombreMicroservicio
            print "Resultado de la petición: "
            print result.content
            print "Código de estado: "
            print result.status_code


        #Mandamos la respuesta que nos devuelve la llamada al microservicio:
        return MensajeRespuesta(message=result.content)

    ##############################################
    #   métodos de IMPARTE                       #
    ##############################################

    @endpoints.method(message_types.VoidMessage, ListaImpartes, path='impartes/getImpartes', http_method='GET', name='impartes.getImpartes')
    def getImpartes(self, unused_request):
        '''
        Devuelve una lista con todos las entidades de la relación Imparte del sistema.
        Llamada desde terminal:
        curl -X GET localhost:8001/_ah/api/helloworld/v1/impartes/getImpartes
        '''
        module = modules.get_current_module_name()
        instance = modules.get_current_instance_id()
        #Leclear decimos a que microservicio queremos conectarnos (solo usando el nombre del mismo), GAE descubre su URL solo.
        url = "http://%s/" % modules.get_hostname(module="microservicio1")
        #Añadimos el recurso al que queremos conectarnos.
        url+="impartes"
        if v:
            print str(url)
        #Al no especificar nada se llama al método GET de la URL.
        result = urlfetch.fetch(url)
        if v:
            print result.content
        listaImpartes = jsonpickle.decode(result.content)

        #Creamos un vector
        impartesItems= []

        for imparte in listaImpartes:
            impartesItems.append(Imparte( id_profesor=str(imparte.get('id_profesor')),
                                              id_clase=str(imparte.get('id_clase')),
                                              id_asignatura=str(imparte.get('id_asignatura'))
                                            ))

        return ListaImpartes(impartes=impartesItems)

    @endpoints.method(Imparte, MensajeRespuesta, path='impartes/insertarImparte', http_method='POST', name='impartes.insertarImparte')
    def insertarImparte(self, request):
        '''
        Introduce una relación Imparte (un procesor que imaparte una asignatura en una clase).
        Ejemplo de llamada en terminal:
        curl -i -d "id_asociacion=1&id_profesor=2" -X POST -G localhost:8001/_ah/api/helloworld/v1/impartes/insertarImparte
        '''

        if v:
            print nombreMicroservicio
            print "Petición POST a impartes.insertarImparte"
            print "Contenido de la petición:"
            print str(request)
            print '\n'

        #Si no tenemos todos los atributos entonces enviamos un error de bad request.
        if request.id_profesor==None or request.id_asociacion==None:
            raise endpoints.BadRequestException('Peticion erronea, faltan datos.')

        #Conformamos la dirección:
        url = "http://%s/" % modules.get_hostname(module="microservicio1")
        #Añadimos el servicio al que queremos conectarnos.
        url+="impartes"


        #Extraemos lo datos de la petición al endpoints
        form_fields = {
          "id_profesor": request.id_profesor,
          "id_asociacion": request.id_asociacion,
        }

        if v:
            print "Llamando a: "+url


        ##Doc de urlfetch: https://cloud.google.com/appengine/docs/python/refdocs/google.appengine.api.urlfetch
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

        return MensajeRespuesta(message=result.content)

    @endpoints.method(ID,MensajeRespuesta,path='impartes/delImparte', http_method='DELETE', name='impartes.delImparte')
    def delImparte(self, request):

        '''
        Elimina una tupla de la relación Imparte del sistema.

        #Ejemplo de borrado de una matrícula:
        curl -d "id=2" -X DELETE -G localhost:8001/_ah/api/helloworld/v1/impartes/delImparte
        {
         "message": "OK"
        }
        '''

        if v:
            print nombreMicroservicio
            print "Petición al método clases.delClase de APIGateway"
            print "Contenido de la petición:"
            print str(request)
            print '\n'

        #Conformamos la dirección:
        url = "http://%s/" % modules.get_hostname(module="microservicio1")


        #Extraemos el argumento id de la petición y la añadimos a la URL
        url+='impartes/'+request.id

        if v:
            print "Llamando a: "+url

        #Realizamos la petición a la url del servicio con el método apropiado DELETE
        result = urlfetch.fetch(url=url, method=urlfetch.DELETE)

        #Infro después de la petición:
        if v:
            print nombreMicroservicio
            print "Resultado de la petición: "
            print result.content
            print "Código de estado: "
            print result.status_code


        #Mandamos la respuesta que nos devuelve la llamada al microservicio:
        return MensajeRespuesta(message=result.content)

    ##############################################
    #   métodos de ASOCIA                       #
    ##############################################

    @endpoints.method(message_types.VoidMessage, ListaAsociaciones, path='asociaciones/getAsociaciones', http_method='GET', name='asociaciones.getAsociaciones')
    def getAsociaciones(self, unused_request):
        '''
        Devuelve una lista con todos las entidades de la relación Asocia del sistema.
        Llamada desde terminal:
        curl -X GET localhost:8001/_ah/api/helloworld/v1/asociaciones/getAsociaciones
        '''
        module = modules.get_current_module_name()
        instance = modules.get_current_instance_id()
        #Leclear decimos a que microservicio queremos conectarnos (solo usando el nombre del mismo), GAE descubre su URL solo.
        url = "http://%s/" % modules.get_hostname(module="microservicio1")
        #Añadimos el recurso al que queremos conectarnos.
        url+="asociaciones"
        if v:
            print str(url)
        #Al no especificar nada se llama al método GET de la URL.
        result = urlfetch.fetch(url)
        if v:
            print result.content
        listaAsociaciones = jsonpickle.decode(result.content)

        #Creamos un vector
        asociacionesItems= []

        for asociacion in listaAsociaciones:
            asociacionesItems.append(Asociacion( id_asociacion=str(asociacion.get('id')),
                                                 id_clase=str(asociacion.get('id_clase')),
                                                 id_asignatura=str(asociacion.get('id_asignatura'))
                                               ))

        return ListaAsociaciones(asociaciones=asociacionesItems)

    @endpoints.method(Asociacion, MensajeRespuesta, path='asociaciones/insertaAsociacion', http_method='POST', name='asociaciones.insertaAsociacion')
    def insertarAsociacion(self, request):
        '''
        Introduce una relación Asocia (una especificación de una asignatura en una clase concreta).
        Ejemplo de llamada en terminal:
        curl -i -d "id_asignatura=2&id_clase=3" -X POST -G localhost:8001/_ah/api/helloworld/v1/asociaciones/insertaAsociacion
        '''

        if v:
            print nombreMicroservicio
            print "Petición POST a asociaciones.insertaAsociacion"
            print "Contenido de la petición:"
            print str(request)
            print '\n'

        #Si no tenemos todos los atributos entonces enviamos un error de bad request.
        if request.id_asignatura==None or request.id_clase==None:
            raise endpoints.BadRequestException('Peticion erronea, faltan datos.')

        #Conformamos la dirección:
        url = "http://%s/" % modules.get_hostname(module="microservicio1")
        #Añadimos el servicio al que queremos conectarnos.
        url+="asociaciones"


        #Extraemos lo datos de la petición al endpoints
        form_fields = {
          "id_asignatura": request.id_asignatura,
          "id_clase": request.id_clase,
        }

        if v:
            print "Llamando a: "+url


        ##Doc de urlfetch: https://cloud.google.com/appengine/docs/python/refdocs/google.appengine.api.urlfetch
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

        return MensajeRespuesta(message=result.content)

    @endpoints.method(ID,MensajeRespuesta,path='asociaciones/delImparte', http_method='DELETE', name='asociaciones.delImparte')
    def delAsociacion(self, request):

        '''
        Elimina una tupla de la relación Imparte del sistema.

        #Ejemplo de borrado de una matrícula:
        curl -d "id=2" -X DELETE -G localhost:8001/_ah/api/helloworld/v1/impartes/delImparte
        {
         "message": "OK"
        }
        '''

        if v:
            print nombreMicroservicio
            print "Petición al método clases.delClase de APIGateway"
            print "Contenido de la petición:"
            print str(request)
            print '\n'

        #Conformamos la dirección:
        url = "http://%s/" % modules.get_hostname(module="microservicio1")


        #Extraemos el argumento id de la petición y la añadimos a la URL
        url+='impartes/'+request.id

        if v:
            print "Llamando a: "+url

        #Realizamos la petición a la url del servicio con el método apropiado DELETE
        result = urlfetch.fetch(url=url, method=urlfetch.DELETE)

        #Infro después de la petición:
        if v:
            print nombreMicroservicio
            print "Resultado de la petición: "
            print result.content
            print "Código de estado: "
            print result.status_code


        #Mandamos la respuesta que nos devuelve la llamada al microservicio:
        return MensajeRespuesta(message=result.content)

    @endpoints.method(ID, AsociacionCompleta,path='asociaciones/getAsociacionCompleta', http_method='GET', name='asociaciones.getAsociacionCompleta')
    def getAsociacionCompleta(self, request):

        '''
        curl -X GET localhost:8001/_ah/api/helloworld/v1/asociaciones/getAsociacionCompleta?id=1
        '''

        module = modules.get_current_module_name()
        instance = modules.get_current_instance_id()
        #Leclear decimos a que microservicio queremos conectarnos (solo usando el nombre del mismo), GAE descubre su URL solo.
        url = "http://%s/" % modules.get_hostname(module="microservicio1")
        #Añadimos el recurso al que queremos conectarnos.
        url+="asociaciones/"+request.id
        if v:
            print str(url)
        #Al no especificar nada se llama al método GET de la URL.
        result = urlfetch.fetch(url)
        if v:
            print result.content

        #Información Asociación Completa
        iac = jsonpickle.decode(result.content)

        print 'IAC recibido: \n'
        print iac

        #Formateamos la información recibida para enviarla.

        #Creamos un par de vectores
        profesores= []
        alumnos = []


        for profesor in iac['profesoresAsociacion']:
            profesores.append(ProfesorSimpleExtendido( nombre=formatText(profesor.get('nombre')), apellidos=formatText(profesor.get('apellidos')), id=str(profesor.get('id')), idImparte=str(profesor.get('idImparte')) ))

        for alumno in iac['alumnosAsociacion']:
            alumnos.append(AlumnoSimpleExtendido( nombre=formatText(alumno.get('nombre')), apellidos=formatText(alumno.get('apellidos')), id=str(alumno.get('id')), idMatricula=str(alumno.get('idMatricula'))))

        return AsociacionCompleta( nombreAsignatura=formatText(iac['nombreAsignatura']), listaProfesores=profesores, listaAlumnos=alumnos, idAsociacion=request.id)





    class Imagen(messages.Message):
        name = messages.StringField(1, required=True)
        image  = messages.BytesField(2, required=True)

    @endpoints.method(Imagen, MensajeRespuesta, path='imagenes/subirImagen', http_method='POST', name='imagenes.subirImagen')
    def subirImagen(self, request):

        print 'Nombre recibido:\n'
        print request.name


        # curl -d "nombre=JuanAntonio" -i -X POST -G localhost:8001/_ah/api/helloworld/v1/imagenes/subirImagen

        '''
        (echo -n '{"image": "'; base64 profile.jpg; echo '"}') | curl -H "Content-Type: application/json"  -d @-  localhost:8001/_ah/api/helloworld/v1/imagenes/subirImagen
        (echo -n '{"image": "'; base64 profile2.jpg; echo '"}') | curl -H "Content-Type: application/json" -d @-  localhost:8001/_ah/api/helloworld/v1/imagenes/subirImagen
        '''

        # curl -d "nombre=prueba" -X POST localhost:8001/_ah/api/helloworld/v1/imagenes/subirImagen

        print "\n ##### IMAGEN RECIBIDA EN API ENDPOINTS: #####\n"
        print '\nImagen en CRUDO: \n'
        print str(request.image)

        import binascii
        stringBase64 = binascii.b2a_base64(request.image)
        print '\nImagen pasada a de Base64 a string: \n'
        print stringBase64

        #print request.image.decode(encoding='UTF-8')

        from manejadorImagenes import ManejadorImagenes
        print 'URL \n'
        url = ManejadorImagenes.CreateFile(request.name, request.image)
        print url

        return MensajeRespuesta( message=str(url) )

    #seguir aqu

APPLICATION = endpoints.api_server([HelloWorldApi])
