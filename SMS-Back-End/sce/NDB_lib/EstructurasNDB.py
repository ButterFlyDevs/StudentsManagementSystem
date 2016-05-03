# -*- coding: utf-8 -*-
from google.appengine.ext import ndb

class ControlAsistencia(ndb.Model):
    # id_ca = ndb.IntegerProperty() --< NO NECESARIO: id_key autoimplementado en ndb
    fecha_hora = ndb.DateTimeProperty() #Queremos que se guarde a la hora
    uniforme = ndb.BooleanProperty()
    retraso_no_justificado = ndb.BooleanProperty()
    retraso_justificado = ndb.BooleanProperty()
    falta = ndb.BooleanProperty()
    id_alumno = ndb.IntegerProperty()
    id_profesor = ndb.IntegerProperty()
    id_clase = ndb.IntegerProperty()
    id_asignatura = ndb.IntegerProperty()

    #Método que devuelve todo lo guardado. En la práctica no se usará
    @classmethod
    def devolver_todo(cls,clave_ancestra):
        return cls.query(ancestor=clave_ancestra).order(-cls.fecha_hora)

#Crear clase NO NDB en un fichero pytthon que sea CA simple y CA complejo. El CA simple tiene estos datos,
#CA complejo tiene estos datos mas lo s nombres de cada uno.
#Se utilizará para devolver los objetos en las funciones

class Resumen_ControlAsistencia(ndb.Model):

    lista_idCA = ndb.IntegerProperty(repeated=True) # La propiedad repeated hace que el campo sea una lista y pueda tomar varios valores, en lugar de solo unof
    fecha_hora = ndb.DateTimeProperty()
    id_profesor = ndb.IntegerProperty()
    id_clase= = ndb.IntegerProperty()
    id_asignatura = ndb.IntegerProperty()

class Alumnos_NombreID(ndb.Model):
    id_alumno = ndb.IntegerProperty(required=True)
    nombre_alumno = StringProperty(required=True)

class Profesores_NombreID(ndb.Model):
    id_profesor = ndb.IntegerProperty(required=True)
    nombre_profesor = StringProperty(required=True)

class Clases_NombreID(ndb.Model):
    id_clase = ndb.IntegerProperty(required=True)
    nombre_clase = StringProperty(required=True)

class Asignaturas_NombreID(ndb.Model):
    id_asignatura = ndb.IntegerProperty(required=True)
    nombre_asignatura = StringProperty(required=True)
