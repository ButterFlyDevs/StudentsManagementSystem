# -*- coding: utf-8 -*-
import webapp2
import json
from tools.GestorAlumnosSQL import GestorAlumnos



#Clase new style
class Profesor(object):
    def __init__(self, nombreInicial, apellidosIniciales):
        self.nombre=nombreInicial
        self.apellidos=apellidosIniciales



class infoProfesor(webapp2.RequestHandler):
    '''
    Devuelve todos los datos de un profesor.
    '''
    def get(self, keywords):
         dni=keywords
         print dni
         #params = extract_params()
         #print params

         '''
         Un sólo objeto:
         '''
         #Declaramos un objeto de tipo profesor
         prof = Profesor('juan','fernandez')
         #Convertimos el objeto a un objteto de tipo JSON
         #salida=json.dumps(prof.__dict__)

         '''
         Ahora probamos con una lista:
         '''
         a = Profesor('juan','fernandez')
         b = Profesor('rocio', 'ayala')

         lista = []
         lista.append(a)
         lista.append(b)
         #Convertimos la lista en una lista de objetos en python
         salida=json.dumps([ob.__dict__ for ob in lista])
         salida='{\"profesores\":'+salida+"}"
         '''
         Salida tiene la siguiente forma:
         {"profesores":[{"nombre": "juan", "apellidos": "fernandez"}, {"nombre": "rocio", "apellidos": "ayala"}]}

         Así tenemos una lista de profesores, donde cada profesor es un elemento completo.
         Después podemos parsear los profesores a una lista:

         r = requests.get('http://localhost:8001/infoProfesor/hey')
         parsed_input=json.loads(r.text)
         Extraemos del json parseado la lista de profesores que tiene incuida.
         lista=parsed_input['profesores']

         (Como podemos imaginar no solo una lista puede llevar, puede contener muchas listas y estructuras mucho más complejas.)

         para recorrer esa lista después con un for:
         for a in lista:
             print a
         que devuelve:
         {u'apellidos': u'fernandez', u'nombre': u'juan'}
         {u'apellidos': u'ayala', u'nombre': u'rocio'}

         O bien acceder a alguno de sus elmentos:
         >>> for a in lista:
            ...     print a['nombre']
            ...
            juan
            rocio

         '''



         self.response.write(salida)

'''
r = requests.get('http://localhost:8001/infoProfesor')
>>> r
<Response [404]>
>>> r = requests.get('http://localhost:8001/infoProfesor/hey')
>>> r
<Response [200]>
>>> r.json()
{u'apellidos': u'antonio', u'nombre': u'juan'}

'''

## CLASE QUE PROCESA EL RECURSO /alumnos
class Alumnos(webapp2.RequestHandler):


    '''
    Procesa las peticiones GET de argumento /todos
    '''
    def get(self, keywords):

        if keywords=='todos':
            '''
            Prueba en terminal:
             curl -i -H 'content-type:application/json' -X GET localhost:8001/alumnos/todos
            '''
            #Recuperamos lo necesario de la base de datos.
            listaAlumnos = GestorAlumnos.getAlumnos()

            #Convertimos la lista de objetos en una lista de objetos JSON serializandolos
            salida=json.dumps([ob.__dict__ for ob in listaAlumnos])
            #Añadimos una cabecera para identificarlos dentro del JSON (esto debería poder hacerse a más alto nivel)
            salida='{\"alumnos\":'+salida+"}"
            #Devolvemos la respuesta
            self.response.write(salida)
        else:
            self.response.write("Petición no procesable.")

    '''
    Procesa las peticiones de tipo POSt:

        -> addAlumno 

    '''
    def post(self, keywords):

        '''
        Ubuntu> curl --data "nombre=Alan&apellidos=Turing" localhost:8001/alumnos/addAlumno
        AÑADIENDO AL ALUMNO: Alan Turing

        '''
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
    ('/alumnos/([^/]+)/?', Alumnos)
], debug=True)



'''
Apuntes extra:

Ubuntu> curl -H 'content-type:application/json' localhost:8001/alumnos/todos | grep }| python -mjson.tool
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   242  100   242    0     0   8494      0 --:--:-- --:--:-- --:--:--  8642
{
    "alumnos": [
        {
            "dni": "Dominguez S\u00e1bado",
            "nombre": "Susana"
        },
        {
            "dni": "grillo",
            "nombre": "pepito"
        },
        {
            "dni": "mengatnito",
            "nombre": "fulanito"
        },
        {
            "dni": "Moreno Rubio",
            "nombre": "Andr\u00e9s"
        },
        {
            "dni": "mengatnito",
            "nombre": "yeahh"
        }
    ]
}


'''
