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

    #Método que devuelve todo lo guardado
    @classmethod
    def devolver_todo(cls,clave_ancestra):
        return cls.query(ancestor=clave_ancestra).order(-cls.fecha_hora)


class Resumen_ControlAsistencia(ndb.Model)

class Alumnos_NombreID(ndb.Model)

class Profesores_NombreID(ndb.Model)

class Clases_NombreID(ndb.Model)

class Asignaturas_NombreID(ndb.Model):
