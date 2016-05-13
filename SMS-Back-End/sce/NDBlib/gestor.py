# -*- coding: utf-8 -*-

'''
import EstructurasNDB.ControlAsistencia
import EstructurasNDB.Resumen_ControlAsistencia
import EstructurasNDB.Alumnos_NombreID
import EstructurasNDB.Profesores_NombreID
import EstructurasNDB.Clases_NombreID
import EstructurasNDB.Asignaturas_NombreID
import Estructuras
'''
from EstructurasNDB import *
import datetime

#Para activar/desactivar el modo verbose para muestra de mensajes.
v = 1
libName='\n ## Gestor NDB ##'


def parseBoolean(cadena):
    if cadena=='True' or cadena== 1 or cadena == '1' :
        return True
    if cadena=='False' or cadena == 0 or cadena == '0' :
        return False


class Gestor:

    @classmethod
    def insertar_prueba(self):

        print '\n\n Insertando prueba \n\n'

        prueba = Prueba()
        prueba.texto='Hola'

        #Cuando insertamos la entidad en el datastore nos devuelve la clave con la que puede ser depués recuperada
        prueba_key = prueba.put()

        pruebaDev = prueba_key.get()
        print pruebaDev




    @classmethod
    def obtenerALLCA(self):
        '''
        Devuelve una lista completa con todos los controles de asistencia.
        '''
        listaCA = []
        listaCA = ControlAsistencia.devolver_todo().fetch(100000)

        return listaCA

    @classmethod
    def obtenerControlAsistencia(id):
        pass

    @classmethod
    def obtenerResumenControlAsistencia(idProfesor, idASignatura, idClase, fechaHora):
        '''
        Debe devolver también nombres (DEBE DEVOLVER UN RCA_complejo)
        '''
        pass


    ###
    #Métodos de la inserccion de un control de asistencia completo.
    ###

    @classmethod
    def insertarConjuntoControlAsistencia(self, listaAsistencias):
        '''
        Inserta en el sistema un control de asistencia (conjunto de ellos) compuesto por al menos un
        control de asistencia de un estudiante(los llamamos igual).
        Recibimos una lista con los controles.
        '''
        if v:
            print libName
            print " Llamada a insertarConjuntoControlAsistencia "
            print listaAsistencias

        #Creamos una lista donde guardaremos las keys que la base de datos nos devuelva al guardar los controles.
        keys = []

        #Establecemos el datetime para usar el mismo en todas las asistencias al guardarlas, cogiéndolo del sistema.
        fechahora = datetime.datetime.now()
        if v:
            print 'Datetime usado:'
            print fechahora

        #Recorremos todos los elementos de la lista pasada
        for asistencia in listaAsistencias:
            #Insertarmos una asistencia en el sistema con una función y guardamos su salida en la lista de keys.
            keys.append(Gestor.insertarControlAsistencia(asistencia, fechahora))

        '''
        Una vez que se han introducido las asistencias en la tabla ControlAsistencia tenemos que crear un resumen
        en la tabla ResumenControlAsistencia y para eso usamos el método insertarResumenControlAsistencia. Para extraer
        los tres últimos parámetros usamos el primer control pasado en la lista.
        '''

        keyResumen=Gestor.insertarResumenControlAsistencia(keys, fechahora, (listaAsistencias[0])['id_profesor'],
                                                                 (listaAsistencias[0])['id_asignatura'],
                                                                 (listaAsistencias[0])['id_clase']
                                               )

        return 'OK'

    @classmethod
    def insertarControlAsistencia(self, control, datetime):
        '''
        Inserta una asistencia en la tabla ControlAsistencia del datastore.
        Devuelve la clave de objeto introducido.
        '''

        #Info de seguimiento
        if v:
            print libName
            print " Llamada a insertarControlAsistencia con params: "
            print locals()
            print '\n'

        #Se crea una instancia del modelo
        nuevoCA = ControlAsistencia()

        #Se rellena de datos, ajustándolos a los que esperamos.
        nuevoCA.fecha_hora=datetime #Usamos directamente la fecha y hora que nos pasan.
        nuevoCA.asistencia=parseBoolean(control['asistencia'])
        nuevoCA.retraso=parseBoolean(control['retraso'])
        nuevoCA.retraso_tiempo=int(control['retraso_tiempo'])
        nuevoCA.retraso_justificado=parseBoolean(control['retraso_justificado'])
        nuevoCA.uniforme=parseBoolean(control['uniforme'])
        nuevoCA.id_alumno=int(control['id_alumno'])
        nuevoCA.id_profesor=int(control['id_profesor'])
        nuevoCA.id_clase=int(control['id_clase'])
        nuevoCA.id_asignatura=int(control['id_asignatura'])

        #Se guarda en el data store
        nuevoCA_clave = nuevoCA.put()

        #Info de seguimiento
        if v:
            print libName
            print " Return de insertarControlAsistencia: "+str(nuevoCA_clave)+'\n'

        return nuevoCA_clave

    @classmethod
    def insertarResumenControlAsistencia(self, listaIdCA, fechaHora,idProfesor,idASignatura,idClase):
        #Info de seguimiento
        if v:
            print libName
            print " Llamada a insertarResumenControlAsistencia con params: "
            print locals()
            print '\n'

        #Se crea una instancia del modelo
        nuevoRCA = ResumenControlAsistencia()

        #Se rellena de datos, ajustándolos a los que esperamos.
        nuevoRCA.lista_idCA=listaIdCA
        nuevoRCA.fecha_hora=fechaHora
        nuevoRCA.id_profesor=idProfesor
        nuevoRCA.id_clase=idClase
        nuevoRCA.id_asignatura=idASignatura


        #Se guarda en el data store
        nuevoRCA_clave = nuevoRCA.put()

        #Info de seguimiento
        if v:
            print libName
            print " Return de insertarResumenControlAsistencia: "+str(nuevoRCA_clave)+'\n'

        return nuevoRCA_clave


    @classmethod
    def obtenerNombreAlumnos(idAlumnos):
        pass

    @classmethod
    def obtenerNombreProfesores(idProfesor):
        pass

    @classmethod
    def obtenerNombreClases(idClase):
        pass

    @classmethod
    def obtenerNombreAsignaturas(idAsignatura):
        pass
