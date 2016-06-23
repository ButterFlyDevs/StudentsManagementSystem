# -*- coding: utf-8 -*-
#####################################################
## Mensajes del servicio de Control de Estudiantes ##
#####################################################
"""
Estructura de mensajes intercambiados en el servicio de Control de estudiantes (sce)
"""
from protorpc import messages
from protorpc import message_types

class MicroControlAsistencia(messages.Message):
    asistencia = messages.IntegerField(1, required=True)
    #Si el retraso es 0: no hay retraso 10: retraso de 10 min 20: retraso de 20 min o más
    retraso = messages.IntegerField(2, required=True)
    retrasoTiempo = messages.IntegerField(3, required=True)
    retrasoJustificado = messages.IntegerField(4, required=True)
    uniforme =  messages.IntegerField(5, required=True)
    id = messages.IntegerField(6, required=True)
    #Campo solo necesario para los controles de asistencia de salida, proceso: obtenerControlAsistencia
    nombreAlumno = messages.StringField(7)

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
    fecha = messages.StringField(8)

class ResumenControlAsistencia(messages.Message):
    key = messages.IntegerField(1, required=True)
    fecha = messages.StringField(2)
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

#### FIN DE LOS MENSAJES PARA EL SCE
