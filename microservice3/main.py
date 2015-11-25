# -*- coding: utf-8 -*-
import webapp2
import json

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



app = webapp2.WSGIApplication([
    ('/infoProfesor/([^/]+)/?', infoProfesor)
], debug=True)



'''
Ejecución de prueba:
curl -H 'content-type:application/json' localhost:8080/infoProfesor/prueba
'''
