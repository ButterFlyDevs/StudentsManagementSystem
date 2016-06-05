# -*- coding: utf-8 -*-
"""
Fichero de definición de la API REST del microservicio 1 SBD, que ofrece la interfaz de conexión con el microservicio
y que en principio solo es una pasarela a la interfaz de conexión con la BD a través de la APIDB.
"""
#Framework que vamos a usar para implementar la API Rest del microservicio. Apenas se va a utilizar toda la funcionalidad de la librería.
import webapp2
import json
from APIDB.GestorAlumnosSQL import GestorAlumnos
#Para la conversión de objetos python a objetos JSON enviables por http usamos la librería jsonpickle.
import jsonpickle

class Alumnos(webapp2.RequestHandler):
    '''
    Manejador de peticiones REST al recurso Alumnos, /alumnos, usando una forma estandar de uso  de parámetros.
    #Responde a http://localhost:8002/alumnos o  curl -X GET http://localhost:8002/alumnos
    '''

    '''
    Si quisiéramos pasar parámetros
    # curl -d "dni=454545" -X GET -G  http://localhost:8080/alumnos
    que equivale a hacer la peticion a http://localhost:8080/alumnos?dni=9
    '''
    def get(self):
        """
        Gestiona las peticiones de tipo get (DAME-QUIERO) al recurso Alumnos


        /alumnos Devuelve una lista con todos los alumnos de la base de datos.
        /alumnos?dni=<dni del alumno> Devuelve todos los datos de un alumno en concreto.

        /alumnos/asignaturas?dni=<dniAlumno> Devuelve todas las asignaturas en la que está matriculado el estudiante.

        /alumnos/profesores?dni=<dniAlumno> Devuelve una lista con todos los profesores que imparten clase a ese alumno



        """
        #Si no se pasa como parámetro nada, se está pidiendo una lista simplificada de todos los alumnos de la base de datos.
        '''
        http://localhost:8080/alumnos
        '''
        if(self.request.get('dni')==''):

            print ("GET ALL ALUMNOS #######################")
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

        #En otro caso, se está pasando el dni del que se quiere toda su información al completo.
        else:
            print ("GET UN ALUMNO #######################")
            #Recuperamos el alumno pedido.
            alumno = GestorAlumnos.getAlumno(self.request.get('dni'))

            if(alumno!='Elemento no encontrado'):
                print "FECHA NACIMIENTO"
                #Tenemos que hacer esto para que no haya problemas al codificar con JSON el tipo de dato fecha nacimiento
                alumno.fecha_nac=str(alumno.fecha_nac)
                print alumno.fecha_nac

            #Si se trata de un error entonces se envía el error que nos devuelve el GestorAlumnos directamente

            #Enviamos el resultado en formato JSON
            self.response.write(jsonpickle.encode(alumno))

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

    def put(self):
        '''
        Recursos de tipo update:

        /alumnos?dni=<dniAlumno>

        '''
        self.response.write('update')


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


#Manejador de URLs donde asociamos cada recurso a una clase.
app = webapp2.WSGIApplication([

    # ALUMNOS #
    ('/alumnos', Alumnos),#Recurso colección alumnos
    (r'/alumnos/(8letrasy1numero)',Alumno) #Recurso entidad alumno, dentro de la colección Alumnos.


], debug=True)
