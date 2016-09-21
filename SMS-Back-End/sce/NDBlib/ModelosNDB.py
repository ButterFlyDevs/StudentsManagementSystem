# -*- coding: utf-8 -*-
"""
Fichero de definición de los modelos de la base de datos, haciendo
uso de los `tipos NDB <https://cloud.google.com/appengine/docs/python/ndb/entity-property-reference>`_ del Cloud DataStore.

Existen dos grupos de modelos.


    * Modelos de datos:

        Aquellos modelos que "modelan" los datos de la base de datos, en este caso los controles de asistencia, que tratados como una
        sola entidad en la IU aquí por motivos de eficiencia se modelan como dos entidades, microControlAsistencia (control sobre
        un alumno concreto bajo unas características concretas) y resumenControlAsistencia (conjutno de referencias a microControles con
        unas características añadidas concretas). Ámbos, el resumen y un número n de microControles forman un Control de Asistencia.

        * **microControlAsistencia**
        * **resumenControlAsistencia**

    * Modelos de referencia:

        Modelos que sirven de referencia a los nombres de estas entidades en la base de datos relacional (que es quien llama a grabarlos y
        modificarlos aquí) y que se usan declarados de forma independiente para ahorrar espacio (evitando duplicidad) y eficacia (evitando
        escrituras masivas y modificaciones cuando estos cambien).

        * **Alumno**
        * **Profesor**
        * **Clase**
        * **Asignatura**

"""
from google.appengine.ext import ndb

# Modelos de datos

class microControlAsistencia(ndb.Model):
    """
    Control de asistencia de un alumno concreto en una clase y asignatura con profesor concretos (por eso lo llamamos micro, el CA
    general hace referencia a todos los mcas que se hacen en un control).

    Aunque se llama *de Asistencia* se salvan más datos que la asistencia, como el si el alumno ha traido uniforme
    o no o si el retraso (en caso de tenerlo) es justificado, pero se usa generalizadamente ese nombre.
    """

    fechaHora = ndb.DateTimeProperty()
    """Fecha y hora a la que se ha realizado el control de asistencia **(ndb.DateTimeProperty)** ."""
    asistencia = ndb.BooleanProperty()
    """Registra si el alumno ha asistido o no a clase **(ndb.BooleanProperty)** ."""
    uniforme = ndb.BooleanProperty()
    """Registra si el alumno ha asistido con o sin uniforme **(ndb.BooleanProperty)** ."""
    retraso = ndb.IntegerProperty()
    """Registra si el alumno ha llegado o no con retraso **(ndb.IntegerProperty)** . """
    retrasoTiempo= ndb.IntegerProperty()
    """Registra el tiempo del retraso en caso de que este se haya producido.
    Si el alumno no ha llegado con retraso será un 0, pero puede ser un retraso de 10 min o de 20 min o mas en cuyo caso será 10 o 20
    **(ndb.IntegerProperty)** . """
    retrasoJustificado = ndb.BooleanProperty()
    """Registra si el retraso (en caso de existir) es justificado **(ndb.BooleanProperty)** ."""
    idAlumno = ndb.IntegerProperty()
    """Identificador del alumno implicado **(ndb.IntegerProperty)**."""
    idProfesor = ndb.IntegerProperty()
    """Identificador del profesor implicado **(ndb.IntegerProperty)** ."""
    idClase = ndb.IntegerProperty()
    """Identificador de la clase implicada **(ndb.IntegerProperty)** ."""
    idAsignatura = ndb.IntegerProperty()
    """Identificador de la asignatura implicada **(ndb.IntegerProperty)** ."""

    #Método que devuelve todo lo guardado. En la práctica no se usará
    @classmethod
    def devolver_todo(cls):
        return cls.query().order(-cls.fecha_hora)

class resumenControlAsistencia(ndb.Model):
    """
    Objeto que representa el reseumen de un control de asistencia (los datos más importantes), un resumen de los microcontroles de
    los alumnos y los datos relevantes a cuando se hizo el control. Aunque cada mc compone una entidad en si el resumen abstrae
    la idea de control en conjunto, compuesto de muchos mcs.
    """

    listaMCAs = ndb.KeyProperty(repeated=True) # La propiedad repeated hace que el campo sea una lista y pueda tomar varios valores, en lugar de solo unof
    """Lista de microcontroles que representan un control de asistencia **(ndb.KeyProperty(repeated=True))** ."""
    fechaHora = ndb.DateTimeProperty()
    """Fecha y hora a la que se ha realizado el control de asistencia **(ndb.DateTimeProperty)** ."""
    idProfesor = ndb.IntegerProperty()
    """Identificador del profesor implicado **(ndb.IntegerProperty)** ."""
    idClase = ndb.IntegerProperty()
    """Identificador de la clase implicada **(ndb.IntegerProperty)** ."""
    idAsignatura = ndb.IntegerProperty()
    """Identificador de la asignatura implicada **(ndb.IntegerProperty)** ."""

# Modelos de referencia

class Alumno(ndb.Model):
    """
    Objeto que almacena una referencia al nombre completo de un **Alumno** almacenado en el SBD y que
    solo es útil para no tener que llamar al otro servicio constantemente, por eso se conocen como entidades referencia.
    """
    idAlumno = ndb.IntegerProperty(required=True)
    """Identificador del alumno en la BD relacional **(ndb.IntegerProperty)** ."""
    nombreAlumno = ndb.StringProperty(required=True)
    """Nombre del alumno en la BD relacional **(ndb.StringProperty)** ."""

class Profesor(ndb.Model):
    """
    Objeto que almacena una referencia al nombre completo de un **Profesor** almacenado en el SBD y que
    solo es útil para no tener que llamar al otro servicio constantemente, por eso se conocen como entidades referencia.
    """
    idProfesor = ndb.IntegerProperty(required=True)
    """Identificador del profesor en la BD relacional **(ndb.IntegerProperty)** ."""
    nombreProfesor = ndb.StringProperty(required=True)
    """Nombre del profesor en la BD relacional **(ndb.StringProperty)** ."""

class Clase(ndb.Model):
    """
    Objeto que almacena una referencia al nombre completo de una **Clase** almacenado en el SBD y que
    solo es útil para no tener que llamar al otro servicio constantemente, por eso se conocen como entidades referencia.
    """
    idClase = ndb.IntegerProperty(required=True)
    """Identificador de la clase en la BD relacional **(ndb.IntegerProperty)** ."""
    nombreClase = ndb.StringProperty(required=True)
    """Nombre de la clase en la BD relacional **(ndb.StringProperty)** ."""

class Asignatura(ndb.Model):
    """
    Objeto que almacena una referencia al nombre completo de una **Asignatura** almacenado en el SBD y que
    solo es útil para no tener que llamar al otro servicio constantemente, por eso se conocen como entidades referencia.
    """
    idAsignatura = ndb.IntegerProperty(required=True)
    """Identificador de la asignatura en la BD relacional **(ndb.IntegerProperty)** ."""
    nombreAsignatura = ndb.StringProperty(required=True)
    """Nombre de la asignatura en la BD relacional **(ndb.StringProperty)** ."""
