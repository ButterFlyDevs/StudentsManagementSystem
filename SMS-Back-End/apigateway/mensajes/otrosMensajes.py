# -*- coding: utf-8 -*-
"""
# Mensajes del servicio de Control de Estudiantes
Estructura de mensajes intercambiados en el servicio de Control de estudiantes (sce)
"""
import endpoints
from protorpc import messages
from protorpc import message_types

class MensajeRespuesta(messages.Message):
    message = messages.StringField(1)

#Mensaje que usamos para devolver la información de estado sobre la creación de alguna entidad en el sistema y además devuelve el id en sistema de la identidad creada. (Como por ejemplo en la insercción de un alumno)
class StatusID(messages.Message):
    status = messages.StringField(1)
    statusCode = messages.StringField(2)
    idEntidad = messages.IntegerField(3)

class URL(messages.Message):
    url = messages.StringField(1)

class MensajePeticion(messages.Message):
    message = messages.StringField(1)
"""
Como vemos, no aparecen argumentos en el cuerpo de la petición ya que se trata
de una petición de tipo GET.
"""

#######################################
## TIPOS DE MENSAJES QUE MANEJA LA API##
#######################################

"""
A continuación se implementa la estrutura de cada tipo de mensaje que se puede enviar o recibir en
el proyecto en el microservicio de apigateway.
"""

class Alumno(messages.Message):
    nombre = messages.StringField(1)
    apellidos = messages.StringField(2)
    id = messages.StringField(3)

class AlumnoCompleto(messages.Message):
    id = messages.StringField(1)
    nombre = messages.StringField(2)
    apellidos = messages.StringField(3)
    dni = messages.StringField(4)
    direccion = messages.StringField(5)
    localidad = messages.StringField(6)
    provincia = messages.StringField(7)
    fecha_nacimiento = messages.StringField(8)
    telefono = messages.StringField(9)
    imagen = messages.StringField(10)

class ID(messages.Message):
    id = messages.StringField(1)

#Un nuevo tipo de mensaje para el profesor simple que añade un poco de información necesaria
class ProfesorSimpleExtendido(messages.Message):
    nombre = messages.StringField(1)
    apellidos = messages.StringField(2)
    id = messages.StringField(3)
    idImparte = messages.StringField(4)

class AlumnoSimpleExtendido(messages.Message):
    nombre = messages.StringField(1)
    apellidos = messages.StringField(2)
    id = messages.StringField(3)
    idMatricula = messages.StringField(4)




#Definimos un tipo especial de mensaje
class AsociacionCompleta(messages.Message):
    nombreAsignatura = messages.StringField(1)
    listaProfesores = messages.MessageField(ProfesorSimpleExtendido, 2, repeated=True)
    listaAlumnos = messages.MessageField(AlumnoSimpleExtendido, 3, repeated=True)
    idAsociacion = messages.StringField(4)

class salidaLogin(messages.Message):
    idUser = messages.StringField(1, required=True)
    nombre = messages.StringField(2, required=True)
    rol = messages.StringField(3, required=True)



class DatosEntidadGenerica(messages.Message):
    """
    Todos los datos que se pueden manejar como entidades.
    """
    nombre = messages.StringField(1)
    apellidos = messages.StringField(2)
    dni = messages.IntegerField(3)
    direccion = messages.StringField(4)
    localidad = messages.StringField(5)
    provincia = messages.StringField(6)
    fechaNacimiento = messages.StringField(7)
    telefono = messages.IntegerField(8)
    imagen = messages.StringField(9)
    idEntidad = messages.StringField(10)
    curso = messages.IntegerField(11)
    grupo = messages.StringField(12)
    nivel = messages.StringField(13)

    #Para la insercción de datos de relación
    idClase = messages.IntegerField(14)
    idAsignatura = messages.IntegerField(15)
    idProfesor = messages.IntegerField(16)
    idAlumno = messages.IntegerField(17)
    idAsociacion = messages.IntegerField(18)

class Entidad(messages.Message):
    tipo = messages.StringField(1)
    datos = messages.MessageField(DatosEntidadGenerica, 2)

class ListaEntidades(messages.Message):
    entidades = messages.MessageField(DatosEntidadGenerica, 1, repeated=True)

class UserMessage(messages.Message):
    tipo = messages.StringField(1)
    email = messages.StringField(2)
    username = messages.StringField(3)

class MensajeModificacionEntidad(messages.Message):
    tipo = messages.StringField(1)
    idEntidad = messages.IntegerField(2)
    campoACambiar = messages.StringField(3)
    nuevoValor = messages.StringField(4)

ID_RESOURCE = endpoints.ResourceContainer(
    message_types.VoidMessage,
    tipo=messages.StringField(1, variant=messages.Variant.STRING, required=True),
    idEntidad=messages.StringField(2))

Recursosv2 = endpoints.ResourceContainer(
    tipoBase = messages.StringField(1, required=True),
    idEntidad = messages.StringField(2, required=True),
    tipoBusqueda = messages.StringField(3, required=True)
    )


class Login(messages.Message):
    username = messages.StringField(1, required=True)
    password = messages.StringField(2, required=True)


class Imagen(messages.Message):
    tipo = messages.StringField(1, required=True)
    idEntidad = messages.StringField(2, required=True)
    imagen  = messages.BytesField(3, required=True)

class AlumnoCompletoConImagen(messages.Message):
    id = messages.StringField(1)
    nombre = messages.StringField(2)
    apellidos = messages.StringField(3)
    dni = messages.StringField(4)
    direccion = messages.StringField(5)
    localidad = messages.StringField(6)
    provincia = messages.StringField(7)
    fecha_nacimiento = messages.StringField(8)
    telefono = messages.StringField(9)
    #En esta ocasión la imagen no es una URL sino los Bytes en crudo.
    imagen  = messages.BytesField(10)
