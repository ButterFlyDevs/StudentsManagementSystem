# -*- coding: utf-8 -*-
import webapp2
import json
from tools.GestorAlumnosSQL import GestorAlumnos
import jsonpickle


## CLASE QUE PROCESA EL RECURSO /alumnos usando una forma estandar de uso  de parámetros.
#Responde a http://localhost:8002/alumnos o  curl -X GET http://localhost:8002/alumnos

class Alumnos(webapp2.RequestHandler):
    """Manejador de peticiones a Alumnos"""

    # curl -X GET http://localhost:8002/alumnos
    def get(self):
        """
        Devuelve una lista con todos los alumnos almacenados en la base de datos.
        """

        #Se está pidiendo que se devuelvan todos los alumnos
        listaAlumnos = GestorAlumnos.getAlumnos()


        #Una vez que tenemos la lista de aĺumnos convertimos los datos a JSON para enviarlos
        salida=""
        for alumno in listaAlumnos:
            salida+= str(json.dumps(alumno.__dict__))

        #print "Imprimiendo lista de alumnos"
        obj = jsonpickle.encode(listaAlumnos)
        #print str(obj)

        #Los enviamos
        self.response.write(obj)

    # curl -d "nombre=JuanAntonio&dni=456320" -X POST http://localhost:8002/alumnos
    #Gestión de las peticiones post.
    def post(self):
        """
        Función para añadir un nuevo alumno a la base de datos.
        """

        print ("post in alumnos")
        print self.request.get('nombre')
        print self.request.get('dni')

        #Grabamos los datos en la base de datos:

        salida=GestorAlumnos.nuevoAlumno(self.request.get('nombre'), self.request.get('dni'))


        #Recogemos los atributos de la petición y los imprimimos
        #self.response.write("nombre: "+self.request.get('nombre')+"\n")
        #self.response.write("dni: "+self.request.get('dni')+"\n")
        '''
        Salida:
        nombre: JuanAntonio
        dni: 456320
        '''
        self.response.write(salida)

    def delete(self):
        """
        Función para eliminar un alumno
        Puede llamarse, pasándole parámetros desde terminal así:
        #curl -d "dni=456320" -X DELETE -G http://localhost:8002/alumnos
        """
        print "LLAMADA EN MAIN"+self.request.get('dni')+"yeah"
        #self.response.write("eliminando\n")
        #self.response.write("dni: "+self.request.get('dni')+"\n")
        self.response.write(GestorAlumnos.delAlumno(self.request.get('dni')))

app = webapp2.WSGIApplication([
    ('/alumnos', Alumnos)
], debug=True)
