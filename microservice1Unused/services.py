# -*- coding: utf-8 -*-
from protorpc import messages
from protorpc import remote
from protorpc.wsgi import service


#con este se define la forma en la que se piden las cosas:
#En este caso la petición es lo que se recibe por el primer valor de la pareja.
#Asi cuando se llama  la url con el primer parámetros se coge lo que se pase.

# Create the request string containing the user's name
class PeticionM1(messages.Message):
    #En la petición debe de pasarse como nombre el nombre de la variable que aquí definimos y será esta la que coja su contenido.
    nombre = messages.StringField(1, required=True)

# Creamos el string que forma la respuesta
class RespuestaM1(messages.Message):
    hello = messages.StringField(1, required=True)
    entero = messages.IntegerField(2)

# Create the request string containing the user's name
class PeticionM2(messages.Message):
    #En la petición debe de pasarse como nombre el nombre de la variable que aquí definimos y será esta la que coja su contenido.
    nombre = messages.StringField(1, required=True)

# Creamos el string que forma la respuesta
class RespuestaM2(messages.Message):
    hello = messages.StringField(1, required=True)
    entero = messages.IntegerField(2)


#Definimos el servicio RPC para intercambiar mensajes:
class ServicioPrueba(remote.Service):

    #Añadimos un decorador. Los decoradores reciben por parámetro otras funciones, en este caso otras funciones.
    @remote.method(PeticionM1, RespuestaM1)
    #Cada método de un servicio acepta un mensaje como parámetro y devuelve un único mensaje como respuesta.
    #A este método se llama cuando se usa la url (en local por ejemplo) localhost:8080/ServicioPrueba.metodo1
    def metodo1(self, request):

        #Aquí es donde se procesa y donde se pasa lo que se quiere al mensae de vuelta
        mensaje=('Yeah YeahHello dfdsf there, %s!' % request.nombre)
        numero = 2

        #En la respuesta, será un diccionario con el formato: {"hello":"Yeah YeahHello dfdsf there, request.nombre!", "entero":2}
        return RespuestaM1(hello=mensaje, entero=numero)

    @remote.method(PeticionM2, RespuestaM2)
    def metodo2(self, request):

        #Aquí es donde se procesa y donde se pasa lo que se quiere al mensae de vuelta
        mensaje=('Yeah YeahHello dfdsf there, %s!' % request.nombre)
        numero = 46376

        #En la respuesta, será un diccionario con el formato: {"hello":"Yeah YeahHello dfdsf there, request.nombre!", "entero":2}
        return RespuestaM2(hello=mensaje, entero=numero)


# Map the RPC service and path (/hello)
app = service.service_mappings([('/ServicioPrueba', ServicioPrueba)])


'''
Ejecución:
Ubuntu> curl -H 'content-type:application/json' -d '{"nombre":"test1"}' localhost:9092/ServicioPrueba.metodo1

'''
