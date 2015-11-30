# -*- coding: utf-8 -*-
import webapp2
import json
from tools.GestorAlumnosSQL import GestorAlumnos

## CLASE QUE PROCESA EL RECURSO /alumnos usando una forma estandar de uso  de parámetros.
class Alumnos(webapp2.RequestHandler):


    '''
    Procesa las peticiones GET de argumento /alumnos
    '''
    #def get(self, keywords):
    def get(self):

        #Estudiamos el número de parámetros de la lista:
        #Esto nos va a dar mucho juego a la hora de procesar las peticiones y de ver que quiere el usuario.
        lista = self.request.arguments()
        numParametros=len(lista)
        print "Longitud de la lista: "+str(numParametros)

        #Procesa /alumnos
        if numParametros==0:
            #Se está pidiendo que se devuelvan todos los alumnos
            listaAlumnos = GestorAlumnos.getAlumnos()
            salida=json.dumps([ob.__dict__ for ob in listaAlumnos])
            salida='{\"alumnos\":'+salida+"}"
            #Devolvemos la respuesta
            self.response.write(salida)

        #Procesa el parámetro idAlumno así: /alumnos?idAlumno=XXXXXXXXX
        if numParametros==1:
            #Se está pidiendo información sobre un alumno en concreto.

            #Más sobre request en https://cloud.google.com/appengine/docs/python/tools/webapp/requestclass?csw=1#Request_arguments
            #Extraemos el parámetro para hacer lo que queramos con el.
            idAlumno = self.request.get('idAlumno')

            #Ahora lo buscaríamos en la base de datos y devolveríamos sus datos en caso de encontralo o un mensaje de
            #error controlado.

            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write('Buscando información de alumno con id ' + str(idAlumno)+"\n")

            '''
            Para poder pasarle varios parámetros a la llamada con curl usar la url completa acomillada
            curl -i -H 'content-type:application/json' -X GET "localhost:8001/alumnos?idAlumno=45151515Z"

            '''

        #Ejemplo con el que se pueden pasar dos (pueden ser n) parámetros
        if numParametros==2:
            #Más sobre request en https://cloud.google.com/appengine/docs/python/tools/webapp/requestclass?csw=1#Request_arguments
            nombre = self.request.get('nombre')
            apellidos = self.request.get('apellidos')
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write('Buscando información de' + idAlumno)
            '''
            Para poder pasarle varios parámetros a la llamada con curl usar la url completa acomillada
            curl -i -H 'content-type:application/json' -X GET "localhost:8001/alumnos?nombre=erik&apellidos=gaius"

            '''

    def post(self, keywords):

#Seguir aquí!!

        '''
        Ubuntu> curl --data "nombre=Alan&apellidos=Turing" localhost:8001/alumnos/addAlumno
        AÑADIENDO AL ALUMNO: Alan Turing

        '''
        #keywords='addAlumno'
        if keywords=='addAlumno':

            #Añadimos un usuario a la base de datos:

            #Para eso primero sacamos los datos:
            nombre=self.request.POST['nombre']
            apellidos=self.request.POST['apellidos']

            print nombre+apellidos
            GestorAlumnos.nuevoAlumno(nombre, apellidos)

            '''
            Salida de str:
            [(u'nombre', u'Alan'), (u'apellidos', u'Turing')]
            '''

            self.response.write("AÑADIENDO AL ALUMNO: "+str(nombre)+" "+str(apellidos)+"\n")



app = webapp2.WSGIApplication([
    ('/infoProfesor/([^/]+)/?', infoProfesor),
    #('/alumnos/([^/]+)/?', Alumnos)
    ('/alumnos', Alumnos)
], debug=True)
