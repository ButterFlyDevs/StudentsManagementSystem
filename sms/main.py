# -*- coding: utf-8 -*-

import datetime
import jinja2
import os
import webapp2
import cgi

#from model import Alumno (No funcion

#from tools.gestorElephantDB.GestorProfesoresSQL import GestorProfesores

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
        session = get_current_session()
        nombreUsuario=session.get('nombre',None)

        templateVars = {"sesion" : True, "userAlias":nombreUsuario}

        template=template_env.get_template('templates/registroasignaturas.html')
        self.response.out.write(template.render(templateVars))

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

        session = get_current_session()
        nombreUsuario=session.get('nombre',None)

        templateVars = {"sesion" : True, "userAlias":nombreUsuario}

        template=template_env.get_template('templates/registroalumnos.html')
        self.response.out.write(template.render(templateVars))


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

    def get(self,mensaje='None'):

        #Siempre antes de cargar una página se cargará la cookie de la sesión de usuario
        session = get_current_session()
        nombreUsuario=session.get('nombre',None)
        templateVars = {"sesion" : True, "userAlias":nombreUsuario}
        template=template_env.get_template('templates/registroprofesores.html')

        self.response.out.write(template.render(templateVars))



    def post(self):


        session = get_current_session()

        username=self.request.get('username')
        userpassword=self.request.get('userpassword')

        #Si los campos de login de usuario NO están vacíos es que se está logueando un usuario.
        if(username!='' and userpassword!=''):
            print 'Intentando logear a ',username,' con pass: ', userpassword


            #Si esos campos están rellenos lo que se quiere hacer es loguear, por tanto hay que:

            #1. Comprobar si el usuario está en el sistema.
            #Vamos a usar el password como contraseña
            profesorLogeado=GestorProfesores.getProfesor(userpassword);

            #2. En el caso de que sea así crear su sesión para que se mantenga durante toda su navegación en el sistema.
            if(profesorLogeado!=None):
                print "Profesor logueado"

                #Introducimos el nombre y el dni del usuario logueado en la sesión.
                session['nombre']='juan'
                session['dni']='45601217'
                self.get('')
            else:
                print "Profesor desconocido en el sistema"
                session.terminate()
                self.get('error')
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

        session = get_current_session()
        nombreUsuario=session.get('nombre',None)


        #Obtenemos todos los Alumnos registrados en el sistema.
        resultados = GestorAlumnos.getAlumnos()

        templateVars = {"sesion" : True, "userAlias":nombreUsuario, "alumnos" : resultados }

        template = template_env.get_template('templates/alumnos.html')
        #Cargamos la plantilla y le pasamos los datos cargardos
        self.response.out.write(template.render(templateVars))

class Profesores(webapp2.RequestHandler):

    def get(self):

        session = get_current_session()
        nombreUsuario=session.get('nombre',None)

        #Obtenemos todos los Alumnos registrados en el sistema.
        resultados = GestorProfesores.getProfesores()

        templateVars = {"sesion":True, "userAlias":nombreUsuario, "profesores" : resultados}

        template = template_env.get_template('templates/profesores.html')
        #Cargamos la plantilla y le pasamos los datos cargardos
        self.response.out.write(template.render(templateVars))

class Asignaturas(webapp2.RequestHandler):

    def get(self):

        session = get_current_session()
        nombreUsuario=session.get('nombre',None)

        #Obtenemos todos los Alumnos registrados en el sistema.
        asignaturas = GestorAsignaturas.getAsignaturas()

        templateVars = {"sesion" : True, "userAlias":nombreUsuario, "asignaturas" : asignaturas}

        template = template_env.get_template('templates/asignaturas.html')
        #Cargamos la plantilla y le pasamos los datos cargardos
        self.response.out.write(template.render(templateVars))

class Inicio(webapp2.RequestHandler):
    def get(self, mensaje=None):

        template = template_env.get_template('templates/inicio.html')

        session = get_current_session()

        nombreUsuario=session.get('nombre',None)

        if session.is_active():
            nombreUsuario=session.get('nombre',None)
            templateVars = {"sesion" : True, "userAlias":nombreUsuario}
            self.response.out.write(template.render(templateVars))
        else:
            #No hay sesión de usuario válida y se muestra la pantalla de inicio estática con mensaje de error
            templateVars = {"sesion" : None, "errorLogin" : mensaje}
            self.response.out.write(template.render(templateVars))

    def post(self):


        session = get_current_session()

        username=self.request.get('username')
        userpassword=self.request.get('userpassword')

        #Si los campos de login de usuario NO están vacíos es que se está logueando un usuario.
        if(username!='' and userpassword!=''):
            print 'Intentando logear a ',username,' con pass: ', userpassword


            #Si esos campos están rellenos lo que se quiere hacer es loguear, por tanto hay que:

            #1. Comprobar si el usuario está en el sistema.
            #Vamos a usar el password como contraseña
            #profesorLogeado=GestorProfesores.getProfesor(userpassword);
            profesorLogeado=True

            #2. En el caso de que sea así crear su sesión para que se mantenga durante toda su navegación en el sistema.
            if(profesorLogeado!=None):
                print "Profesor logueado"

                #Introducimos el nombre y el dni del usuario logueado en la sesión.
                session['nombre']='juan'
                session['dni']='45601217'
                self.get()
            else:
                print "Profesor desconocido en el sistema"
                session.terminate()
                self.get('error')
        #Si por el contrario si están vacío no se está logueando al usuario porque no se está introduciendo nada:
        else:
            self.get('error')



class Salir(webapp2.RequestHandler):
    def get(self):
        session = get_current_session()
        if session.is_active():
            session.terminate()
        self.redirect('/')

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
class DetallesAlumno(webapp2.RequestHandler):

    #Por post nos llegan los datos de la petición de un profesor.
    def post(self):


        session = get_current_session()
        nombreUsuario=session.get('nombre',None)


        #Extraemos el profesor por el que nos preguntan del formulario con .get y el nombre del campo y creamos
        #un objeto de tipo profesor que le pasaremos al html para que se muestre allí.

        #Si se está haciendo petición por la información de un profesor

        #Si se está haciendo petición por otros datos
        tipo=self.request.get('tipo')


        #Si no se especifica tipo de petición de información se quiere mostrar sólo la información del profesor.
        if tipo=="":

            dniAlumno = self.request.get('dniAlumno')
            print "DNI ALUMNO -> "+dniAlumno
            alumno = GestorAlumnos.getAlumno(dniAlumno)
            templateVars = {"sesion" : True, "userAlias":nombreUsuario,"alumno" : alumno}
            template = template_env.get_template('templates/detallesAlumno.html')
            #Cargamos la plantilla y le pasamos los datos cargardos
            self.response.out.write(template.render(templateVars))


        #Si se ha hecho post y el formulario incluye el campo tipo alumnos lo que se pide es que se muestre
        # la información de alumnos en la misma página.
        if tipo=="profesores":

            #Obtenemos la información del alumno para seguir mostrándola.
            dniAlumno = self.request.get('dniAlumno')
            alumno = GestorAlumnos.getAlumno(dniAlumno)

            #Obtenemos los profesores que imparten clase a ese alumno
            profesoresQueImpartenClaseAlAlumno = GestorAlumnos.getProfesoresAlumno(dniAlumno)

            templateVars = {"sesion" : True, "userAlias":nombreUsuario,"alumno" : alumno,
                            "profesores" : profesoresQueImpartenClaseAlAlumno}
            template = template_env.get_template('templates/detallesAlumno.html')
            #Cargamos la plantilla y le pasamos los datos cargardos
            self.response.out.write(template.render(templateVars))


        if tipo=="asignaturas":

            #Obtenemos la información del alumno para seguir mostrándola.
            dniAlumno = self.request.get('dniAlumno')
            alumno = GestorAlumnos.getAlumno(dniAlumno)

            asignaturasMatriculadas = GestorAlumnos.getAsignaturasMatriculadas(dniAlumno)

            templateVars = {"sesion" : True, "userAlias":nombreUsuario,"alumno" : alumno,
                            "asignaturas" : asignaturasMatriculadas}
            template = template_env.get_template('templates/detallesAlumno.html')
            #Cargamos la plantilla y le pasamos los datos cargardos
            self.response.out.write(template.render(templateVars))


class DetallesAsignatura(webapp2.RequestHandler):

    #Por post nos llegan los datos de la petición de un profesor.
    def post(self):

        session = get_current_session()
        nombreUsuario=session.get('nombre',None)

        #Extraemos el profesor por el que nos preguntan del formulario con .get y el nombre del campo y creamos
        #un objeto de tipo profesor que le pasaremos al html para que se muestre allí.

        #Si se está haciendo petición por la información de un profesor

        #Si se está haciendo petición por otros datos
        tipo=self.request.get('tipo')


        #Si no se especifica tipo de petición de información se quiere mostrar sólo la información del profesor.
        if tipo=="":

            idAsignatura = self.request.get('idAsignatura')
            asignatura = GestorAsignaturas.getAsignatura(idAsignatura)
            templateVars = {"sesion" : True, "userAlias":nombreUsuario,"asignatura" : asignatura}
            template = template_env.get_template('templates/detallesAsignatura.html')
            #Cargamos la plantilla y le pasamos los datos cargardos
            self.response.out.write(template.render(templateVars))


        #Si se ha hecho post y el formulario incluye el campo tipo alumnos lo que se pide es que se muestre
        # la información de alumnos en la misma página.
        if tipo=="profesores":

            #Obtenemos la información de la asignatura para seguir mostrándola
            asignatura = GestorAsignaturas.getAsignatura(self.request.get('idAsignatura'))

            #Obtenemos los profesores que imparten esa asignatura:
            profesoresQueImpartenLaAsignatura = GestorAsignaturas.getProfesoresQueImpartenLaAsignatura(self.request.get('idAsignatura'))

            templateVars = {"sesion" : True, "userAlias":nombreUsuario,"asignatura" : asignatura,
                            "profesores" : profesoresQueImpartenLaAsignatura}
            template = template_env.get_template('templates/detallesAsignatura.html')
            #Cargamos la plantilla y le pasamos los datos cargardos
            self.response.out.write(template.render(templateVars))


        if tipo=="alumnos":

            #Obtenemos la información de la asignatura para seguir mostrándola
            asignatura = GestorAsignaturas.getAsignatura(self.request.get('idAsignatura'))

            #Obtenemos los alumnos matriculados en esa asignatura
            alumnosMatriculados = GestorAsignaturas.getAlumnosMatriculados(self.request.get('idAsignatura'))

            templateVars = {"sesion" : True, "userAlias":nombreUsuario,"asignatura" : asignatura,
                            "alumnos" : alumnosMatriculados}

            template = template_env.get_template('templates/detallesAsignatura.html')
            #Cargamos la plantilla y le pasamos los datos cargardos
            self.response.out.write(template.render(templateVars))

        if tipo == "herramientas":

            #Dentro de esta sección podríamos hacer otra subsección con otro selección de tipo, como:

            #tipoHerramienta=herramientaMatriculacion, por ejemplo


            #Obtenemos los alumnos matriculados en esa asignatura
            alumnosMatriculados = GestorAsignaturas.getAlumnosMatriculados(self.request.get('idAsignatura'))

            #Obtenemos la información de la asignatura para seguir mostrándola
            asignatura = GestorAsignaturas.getAsignatura(self.request.get('idAsignatura'))
            #Enviamos el activador de la sección de Herramientas, para que se renderice esa zona

            #Una vez dentro de herramientas seleccionamos el tipo que queramos.
            tipoHerramienta = self.request.get('tipoHerramienta')

            '''
            Cuando no se haya seleccionado tipo de herramienta y se entre por primera vez para no mostrar el espacio
            vacío mostramos la herramienta de matriculación.
            '''
            if tipoHerramienta == '':
                print "no hay tipo de herramienta"
                tipoHerramienta = 'mat'

            #tipoHerramienta='desmat'
            print "tipoHerramienta"+str(tipoHerramienta)+"<-"

            '''
            Nomenclatura de la sección de herramientas:
            mat-> sección de matriculación
            desmat -> sección de desmatriculación
            del -> sección de eliminación de la asignatura.
            '''

            templateVars = {"sesion" : True, "userAlias":nombreUsuario,"asignatura" : asignatura,
                            "herramienta" : tipoHerramienta,
                            "alumnosParaMatricular" : alumnosMatriculados}

            template = template_env.get_template('templates/detallesAsignatura.html')
            #Cargamos la plantilla y le pasamos los datos cargardos
            self.response.out.write(template.render(templateVars))


        if tipo == "borradoAsignatura":

            #Borramos la asignatura
            asignatura = GestorAsignaturas.delAsignatura(self.request.get('idAsignatura'))

            #Obtenemos todas las asignaturas registrados en el sistema.
            asignaturas = GestorAsignaturas.getAsignaturas()

            mensaje="eliminacion"

            templateVars = {"asignaturas" : asignaturas,
                            "mensaje" : mensaje}

            template = template_env.get_template('templates/asignaturas.html')
            #Cargamos la plantilla y le pasamos los datos cargardos
            self.response.out.write(template.render(templateVars))



class SubidaAlumnosCSV(webapp2.RequestHandler):

    def post(self):
        file = self.request.get('fichero')
        import csv
        import sys

        f = open(file, 'r')
        csv.register_dialect('prueba', delimiter=',')
        reader = csv.reader(f, dialect='prueba')

        for i in range(10):
                row = reader.next()
                nombre = row[0]
                nombreDividido = nombre.split(',')
                if len(nombreDividido)==2:
                        #print nombreDividido[1],nombreDividido[0]
                        nombre=unicode(nombreDividido[1], errors='replace')
                        apellidos=unicode(nombreDividido[0], errors='replace')

                    #    GestorAlumnos.nuevoAlumno(nombre, apellidos)

                else:
                        print nombreDividido[0]



'''
En esta vamos a intentar hacer lo mismo que en la primera pero sin que la información
se vea en la URL de la página y para eso usaremos post.
'''
class DetallesProfesor2(webapp2.RequestHandler):

    def get(self):
        self.response.write("No debería haber nada aquí :)")

    #Por post nos llegan los datos de la petición de un profesor.
    def post(self):

        session = get_current_session()
        nombreUsuario=session.get('nombre',None)

        #Extraemos el profesor por el que nos preguntan del formulario con .get y el nombre del campo y creamos
        #un objeto de tipo profesor que le pasaremos al html para que se muestre allí.

        #Si se está haciendo petición por la información de un profesor

        #Si se está haciendo petición por otros datos
        tipo=self.request.get('tipo')


        #Si no se especifica tipo de petición de información se quiere mostrar sólo la información del profesor.
        if tipo=="":

            dniProfesor = self.request.get('dniProfesor')
            profesor = GestorProfesores.getProfesor(dniProfesor)
            templateVars = {"sesion" : True, "userAlias":nombreUsuario,"profesor" : profesor}
            template = template_env.get_template('templates/detallesProfesor.html')
            #Cargamos la plantilla y le pasamos los datos cargardos
            self.response.out.write(template.render(templateVars))


        #Si se ha hecho post y el formulario incluye el campo tipo alumnos lo que se pide es que se muestre
        # la información de alumnos en la misma página.
        if tipo=="alumnos":
            dniProfesor = self.request.get('dniProfesor')
            #Obtenemos el objeto profesor para que siga mostrandose en la página.
            profesor = GestorProfesores.getProfesor(dniProfesor)
            #Obtenemos los alumnos a los que imparte clase ese profesor:
            alumnosALosQueDaClaseElProfesor = GestorProfesores.getAlumnosProfesor(dniProfesor)

            templateVars = {"sesion" : True, "userAlias":nombreUsuario,"profesor" : profesor,
                            "alumnos" : alumnosALosQueDaClaseElProfesor}
            template = template_env.get_template('templates/detallesProfesor.html')
            #Cargamos la plantilla y le pasamos los datos cargardos
            self.response.out.write(template.render(templateVars))


        if tipo=="asignaturas":
            dniProfesor = self.request.get('dniProfesor')
            profesor = GestorProfesores.getProfesor(dniProfesor)
            asignaturasImpatidasPorProfesor = GestorProfesores.getAsignaturasImpartidasProfesor(dniProfesor)
            templateVars = {"sesion" : True, "userAlias":nombreUsuario,"profesor" : profesor,
                            "asignaturas" : asignaturasImpatidasPorProfesor}
            template = template_env.get_template('templates/detallesProfesor.html')
            #Cargamos la plantilla y le pasamos los datos cargardos
            self.response.out.write(template.render(templateVars))


        #self.response.write(dniProfesor)

class Login(webapp2.RequestHandler):

    def get(self):
        template = template_env.get_template('templates/login.html')
        #Cargamos la plantilla y le pasamos los datos cargardos
        self.response.out.write(template.render())





application = webapp2.WSGIApplication([
                                      ('/', Inicio),
                                      ('/login', Login),
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
                                      ('/detallesProfesor2', DetallesProfesor2),
                                      ('/detallesAlumno', DetallesAlumno),
                                      ('/detallesAsignatura', DetallesAsignatura),
                                      ('/subidaAlumnosCSV', SubidaAlumnosCSV),
                                      ('/salir',Salir)
                                      ]
                                      ,debug=True)
