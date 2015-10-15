# -*- coding: utf-8 -*-

import datetime
import jinja2
import os
import webapp2
import cgi


#from model import Alumno (No funciona)
from tools.GestorAlumnos import GestorAlumnos
from tools.GestorProfesores import GestorProfesores

#Vamos a usar el manejador de forms WTForms

#Importamos el módulo necesario para trabajar con la base de datos
from google.appengine.ext import ndb
'''
ndb es una libreria de modelado de datos, que corre completamente en el código de
nuestra aplicación. La librería fue iniciada por Guido van Rsossum.
'''

from gaesessions import get_current_session




template_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.getcwd()))



class RegistroAlumnos(webapp2.RequestHandler):

    def get(self):

        template=template_env.get_template('templates/registroalumnos.html')
        self.response.out.write(template.render())



    def post(self):

        def validaTexto(texto):
            if len(texto)>0:
                return True
            else:
                return False


        nombreUsuario = validaTexto(self.request.get('nombre'))
        apellidosUsuario = validaTexto(self.request.get('apellidos'))

        if not(nombreUsuario and apellidosUsuario):
            template=template_env.get_template('templates/registroalumnos.html')
            template=template_env.get_template('templates/formulario.html')
            self.response.out.write(template.render())
        else:
            #Grabamos los datos en la base de datos.
            GestorAlumnos.nuevoAlumno(self.request.get('nombre'), self.request.get('apellidos'))

            #Enviamos mensaje de aceptación.
            self.response.out.write('<html><body>You wrote:<pre>')
            self.response.out.write(self.request.get('nombre'))
            self.response.out.write('</pre></body></html>')

class Alumnos(webapp2.RequestHandler):

    def get(self):

        #Obtenemos todos los Alumnos registrados en el sistema.
        resultados = GestorAlumnos.getAlumnos()
        alumnos = Alumno.query()
        resultados= alumnos.fetch(10)

        FAVORITES = [ "chocolates", "lunar eclipses", "rabbits" ]
        templateVars = {"favorites" : resultados}

        template = template_env.get_template('templates/alumnos.html')
        #Cargamos la plantilla y le pasamos los datos cargardos
        self.response.out.write(template.render(templateVars))


class MainPage(webapp2.RequestHandler):
    def get(self):
        template = template_env.get_template('templates/inicio.html')
        '''
        user = self.session.get('user')
        template_values = {
            'user': user
            }
        '''
        self.response.out.write(template.render())

class Hello(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello Testing World!')


application = webapp2.WSGIApplication([
                                      ('/', MainPage),
                                      ('/form', Formulario),
                                      ('/alumnos', Alumnos),
                                      ('/hello', Hello)
                                      ]
                                      ,debug=True)
