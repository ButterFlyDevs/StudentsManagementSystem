# -*- coding: utf-8 -*-
import webapp2
import json
from tools.GestorAlumnosSQL import GestorAlumnos

## CLASE QUE PROCESA EL RECURSO /alumnos usando una forma estandar de uso  de parámetros.
class Alumnos(webapp2.RequestHandler):

    def get(self):

        #Se está pidiendo que se devuelvan todos los alumnos
        listaAlumnos = GestorAlumnos.getAlumnos()


        #Una vez que tenemos la lista de aĺumnos convertimos los datos a JSON para enviarlos
        salida=""
        for alumno in listaAlumnos:
            salida+= str(json.dumps(alumno.__dict__))

        #Los enviamos
        self.response.write(salida)


app = webapp2.WSGIApplication([
    ('/alumnos', Alumnos)
], debug=True)
