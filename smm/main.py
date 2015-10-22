# -*- coding: utf-8 -*-

import datetime
import jinja2
import os
import webapp2
import cgi


#from model import Alumno (No funciona)
from tools.GestorAlumnosSQL import GestorAlumnos
from tools.GestorProfesoresSQL import GestorProfesores
from tools.GestorAsignaturasSQL import GestorAsignaturas

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


class RegistroAsignaturas(webapp2.RequestHandler):

    def get(self):

        template=template_env.get_template('templates/registroasignaturas.html')
        self.response.out.write(template.render())

    def post(self):

        def validaTexto(texto):
            if len(texto)>0:
                return True
            else:
                return False


        nombreAsignatura = validaTexto(self.request.get('nombre'))
        idAsignatura = validaTexto(self.request.get('id'))

        if not(nombreAsignatura and idAsignatura):
            template=template_env.get_template('templates/registroasignaturas.html')
            self.response.out.write(template.render())
        else:
            #Grabamos los datos en la base de datos.
            GestorAsignaturas.nuevaAsignatura(self.request.get('nombre'), self.request.get('id'))

            #Enviamos mensaje de aceptación.
            self.response.out.write('<html><body>You wrote:<pre>')
            self.response.out.write(self.request.get('nombre'))
            self.response.out.write('</pre></body></html>')

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
        dniUsuario = validaTexto(self.request.get('dni'))

        if not(nombreUsuario and dniUsuario):
            template=template_env.get_template('templates/registroalumnos.html')
            self.response.out.write(template.render())
        else:
            #Grabamos los datos en la base de datos.
            GestorAlumnos.nuevoAlumno(self.request.get('nombre'), self.request.get('dni'))

            #Enviamos mensaje de aceptación.
            self.response.out.write('<html><body>You wrote:<pre>')
            self.response.out.write(self.request.get('nombre'))
            self.response.out.write('</pre></body></html>')

class RegistroProfesores(webapp2.RequestHandler):

    def get(self):

        #Siempre antes de cargar una página se cargará la cookie de la sesión de usuario
        session = get_current_session()

        template=template_env.get_template('templates/registroprofesores.html')
        self.response.out.write(template.render())



    def post(self):

        username=self.request.get('username')
        userpassword=self.request.get('userpassword')

        #Si los campos de login de usuario NO están vacíos es que se está logueando un usuario.
        if(username!='' and userpassword!=''):
            print 'Intentando logear a ',username,' con pass: ', userpassword


            #Si esos campos están rellenos lo que se quiere hacer es loguear, por tanto hay que:

            #1. Comprobar si el usuario está en el sistema.

            #2. En el caso de que sea así crear su sesión para que se mantenga durante toda su navegación en el sistema.


            self.get()

        #Si por el contrario si están vacío no se está logueando al usuario sino usando otro formulario.

        else:
            def validaTexto(texto):
                if len(texto)>0:
                    return True
                else:
                    return False


            nombreUsuario = validaTexto(self.request.get('nombre'))
            dniUsuario = validaTexto(self.request.get('dni'))

            if not(nombreUsuario and dniUsuario):
                template=template_env.get_template('templates/registroprofesores.html')
                self.response.out.write(template.render())
            else:
                #Grabamos los datos en la base de datos.
                GestorProfesores.nuevoProfesor(self.request.get('nombre'), self.request.get('dni'))

                #Enviamos mensaje de aceptación.
                self.response.out.write('<html><body>You wrote:<pre>')
                self.response.out.write(nombreUsuario)
                self.response.out.write('</pre></body></html>')


class Alumnos(webapp2.RequestHandler):

    def get(self):

        #Obtenemos todos los Alumnos registrados en el sistema.
        resultados = GestorAlumnos.getAlumnos()

        templateVars = {"alumnos" : resultados}

        template = template_env.get_template('templates/alumnos.html')
        #Cargamos la plantilla y le pasamos los datos cargardos
        self.response.out.write(template.render(templateVars))

class Profesores(webapp2.RequestHandler):

    def get(self):

        #Obtenemos todos los Alumnos registrados en el sistema.
        resultados = GestorProfesores.getProfesores()

        templateVars = {"profesores" : resultados}

        template = template_env.get_template('templates/profesores.html')
        #Cargamos la plantilla y le pasamos los datos cargardos
        self.response.out.write(template.render(templateVars))

class Asignaturas(webapp2.RequestHandler):

    def get(self):

        #Obtenemos todos los Alumnos registrados en el sistema.
        resultados = GestorAsignaturas.getAsignaturas()

        templateVars = {"asignaturas" : resultados}

        template = template_env.get_template('templates/asignaturas.html')
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

class HelloWorldHandler(webapp2.RequestHandler):
   def get(self):

     #  session = get_current_session()

       #Extraemos un valor de la sesión, el valor count.
     #  count = session.get('count', 0)


       #Ponemos un valor en la sesión.
     #  session['count'] = count + 1

     #  html=count,'times'

       # Create the handler's response "Hello World!" in plain text.
       self.response.headers['Content-Type'] = 'text/plain'
       #self.response.out.write(html)

       self.response.out.write('Hello Testing World!')

class DetallesProfesor(webapp2.RequestHandler):
    def get(self, dniProfesor):
        self.response.write('This is the ProductHandler. '
            'The product id is %s' % dniProfesor)



'''
En esta vamos a intentar hacer lo mismo que en la primera pero sin que la información
se vea en la URL de la página y para eso usaremos post.
'''
class DetallesProfesor2(webapp2.RequestHandler):
    def get(self):
        self.response.write("2ª funcion")

    def post(self):
        dniUsuario = self.request.get('dniProfesor')
        self.response.write(dniUsuario)

application = webapp2.WSGIApplication([
                                      ('/', MainPage),
                                      ('/registroalumnos', RegistroAlumnos),
                                      ('/registroprofesores', RegistroProfesores),
                                      ('/registroasignaturas', RegistroAsignaturas),
                                      ('/alumnos', Alumnos),
                                      ('/asignaturas', Asignaturas),
                                      ('/profesores', Profesores),
                                      ('/hello', HelloWorldHandler),
                                      #Estamos usando una expresión regular para poder coger parámetros por la URL.
                                      #La idea es poder enviar desde el html un parametro a get de DetallesProfsor para que
                                      #muestre la info detallada de ese profesor. Problema: que la información pasada
                                      #se muestra en la barra del navegador pues forma parte de la URL
                                      (r'/detallesProfesor/(\w+)', DetallesProfesor),
                                      ('/detallesProfesor2', DetallesProfesor2)
                                      ]
                                      ,debug=True)
