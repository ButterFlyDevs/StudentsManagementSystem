# -*- coding: utf-8 -*-
"""
# Mensajes del servicio de Control de Estudiantes
Estructura de mensajes intercambiados en el servicio de Control de estudiantes (sce)
"""
from protorpc import messages
from protorpc import message_types

class MicroControlAsistencia(messages.Message):
    """
    Mensaje que representa el Control de Asistencia que se realiza a un estudiante en concreto, que contiene la información
    elemental del control incluido el nombre del alumno (útil en la UI)
    """
    asistencia = messages.IntegerField(1, required=True)
    """Si el alumno ha asisitido: 1 si no: 0. **(messages.IntegerField)** ."""
    retraso = messages.IntegerField(2, required=True)
    """Si el alumno ha asisitido con retraso: 1 si no: 0. **(messages.IntegerField)** ."""
    retrasoTiempo = messages.IntegerField(3, required=True)
    """Si el alumno ha asisitido con retraso, el tiempo aproximado:
    10 si han sido 10 min. aproxim, 20 si han sido 20 o más minutos. **(messages.IntegerField)** ."""
    retrasoJustificado = messages.IntegerField(4, required=True)
    """Si el alumno ha asisitido con retraso y este es justificado: 1 si no: 0. **(messages.IntegerField)** ."""
    uniforme =  messages.IntegerField(5, required=True)
    """Si el alumno ha asisitido con uniforme: 1 si no: 0. **(messages.IntegerField)** ."""
    idAlumno = messages.IntegerField(6, required=True)
    #Campo solo necesario para los controles de asistencia de salida, proceso: obtenerControlAsistencia
    nombreAlumno = messages.StringField(7)
    """Nombre completo del alumno, sólo útil para los controles de asistencia de salida (para la UI). **(messages.StringField)** ."""

class ControlAsistencia(messages.Message):
    microControlesAsistencia = messages.MessageField(MicroControlAsistencia, 1, repeated=True)
    idProfesor = messages.IntegerField(2, required=True)
    idClase = messages.IntegerField(3, required=True)
    idAsignatura = messages.IntegerField(4, required=True)
    """
    Campos solo necesarios para los controles de asistencia de salida, proceso:
    """
    nombreClase = messages.StringField(5)
    nombreAsignatura = messages.StringField(6)
    nombreProfesor = messages.StringField(7)
    fechaHora = messages.StringField(8)

class ResumenControlAsistencia(messages.Message):
    key = messages.IntegerField(1, required=True)
    fechaHora = messages.StringField(2)
    idClase = messages.IntegerField(3)
    nombreClase = messages.StringField(4)
    idAsignatura = messages.IntegerField(5)
    nombreAsignatura = messages.StringField(6)
    idProfesor = messages.IntegerField(7)
    nombreProfesor = messages.StringField(8)

class ListaResumenesControlesAsistencia(messages.Message):
    resumenes = messages.MessageField(ResumenControlAsistencia, 1, repeated=True)

#Cuando pedimos los resumenes de los controles de asistencia los podemos pedir usando parámetros o sin ellos.
class ParametrosPeticionResumenes(messages.Message):
    idProfesor = messages.IntegerField(1)
    idAsignatura = messages.IntegerField(2)
    idClase = messages.IntegerField(3)
    fechaHora = messages.StringField(4)
