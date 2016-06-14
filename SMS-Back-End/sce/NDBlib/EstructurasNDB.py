# -*- coding: utf-8 -*-
from google.appengine.ext import ndb

class Prueba(ndb.Model):
    texto=ndb.StringProperty()

class microControlAsistencia(ndb.Model):
    """
    Contro de asistencia de un alumno concreto en una clase y asignatura con profesor concretos.

    Aunque se llama ControlAsistencia se salvan más datos que la asistencia, como el si el alumno ha traido uniforme
    o no o si el retraso (en caso de tenerlo) es justificado.
    """

    # id_ca = ndb.IntegerProperty() --< NO NECESARIO: id_key autoimplementado en ndb
    #Fecha y hora a la que se ha realizado el control de asistencia.
    fechaHora = ndb.DateTimeProperty()
    #Si el alumno ha asistido a clase
    asistencia = ndb.BooleanProperty()
    #Si ha traido o no el uniforme.
    uniforme = ndb.BooleanProperty()
    #Si el alumno no ha llegado con retraso será un 0, pero puede ser un retraso de 10 min o de 20 min o mas en cuyo caso será 10 o 20 el valor
    retraso = ndb.IntegerProperty()
    #En caso de llegar con retraso de cuanto se ha tratado. 10 o 20 o + minutos
    retrasoTiempo= ndb.IntegerProperty()
    #En caso de llegar con retraso si este ha sido justificado o no
    retrasoJustificado = ndb.BooleanProperty()

    #Datos de los implicados
    idAlumno = ndb.IntegerProperty()
    idProfesor = ndb.IntegerProperty()
    idClase = ndb.IntegerProperty()
    idAsignatura = ndb.IntegerProperty()

    #Método que devuelve todo lo guardado. En la práctica no se usará

    @classmethod
    def devolver_todo(cls):
        return cls.query().order(-cls.fecha_hora)

#Crear clase NO NDB en un fichero pytthon que sea CA simple y CA complejo. El CA simple tiene estos datos,
#CA complejo tiene estos datos mas lo s nombres de cada uno.
#Se utilizará para devolver los objetos en las funciones

class resumenControlAsistencia(ndb.Model):

    listaMCAs = ndb.KeyProperty(repeated=True) # La propiedad repeated hace que el campo sea una lista y pueda tomar varios valores, en lugar de solo unof
    fechaHora = ndb.DateTimeProperty()
    idProfesor = ndb.IntegerProperty()
    idClase = ndb.IntegerProperty()
    idAsignatura = ndb.IntegerProperty()

class Alumno(ndb.Model):
    """
    Objeto que almacena una referencia al nombre completo de un **Alumno** almacenado en el SBD y que
    solo es útil para no tener que llamar al otro servicio constantemente, por eso se conocen como entidades referencia.
    """
    idAlumno = ndb.IntegerProperty(required=True)
    """Entero *(ndb.IntegerProperty)*"""
    nombreAlumno = ndb.StringProperty(required=True)
    """String *(ndb.StringProperty)*"""

class Profesor(ndb.Model):
    """
    Objeto que almacena una referencia al nombre completo de un **Profesor** almacenado en el SBD y que
    solo es útil para no tener que llamar al otro servicio constantemente, por eso se conocen como entidades referencia.
    """
    idProfesor = ndb.IntegerProperty(required=True)
    """Entero *(ndb.IntegerProperty)*"""
    nombreProfesor = ndb.StringProperty(required=True)
    """String *(ndb.StringProperty)*"""

class Clase(ndb.Model):
    """
    Objeto que almacena una referencia al nombre completo de una **Clase** almacenado en el SBD y que
    solo es útil para no tener que llamar al otro servicio constantemente, por eso se conocen como entidades referencia.
    """
    idClase = ndb.IntegerProperty(required=True)
    """Entero *(ndb.IntegerProperty)*"""
    nombreClase = ndb.StringProperty(required=True)
    """String *(ndb.StringProperty)*"""

class Asignatura(ndb.Model):
    """
    Objeto que almacena una referencia al nombre completo de una **Asignatura** almacenado en el SBD y que
    solo es útil para no tener que llamar al otro servicio constantemente, por eso se conocen como entidades referencia.
    """
    idAsignatura = ndb.IntegerProperty(required=True)
    """Entero *(ndb.IntegerProperty)*"""
    nombreAsignatura = ndb.StringProperty(required=True)
    """String *(ndb.StringProperty)*"""
