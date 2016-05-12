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

#Para activar/desactivar el modo verbose para muestra de mensajes.
v = 1
libName='\n ## Gestor NDB ##'

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

    @classmethod
    def insertarControlAsistencia(self, fechaHora, asistencia, uniforme, retraso, retraso_tiempo,
                                  retraso_justificado,  idAlumno, idProfesor, idClase, idASignatura):
        '''
        Inserta un control de asistencia en la tabla ControlAsistencia del datastore.
        Devuelve la clave de objeto introducido.
        '''

        #Info de seguimiento
        if v:
            print libName
            print " Llamada a insertarControlAsistencia con params: "
            print locals()
            print '\n'


        #Se crea el modelo
        nuevoCA = ControlAsistencia()

        #Se rellena de datos
        nuevoCA.fecha_hora=fechaHora
        nuevoCA.asistencia=asistencia
        nuevoCA.uniforme=uniforme
        nuevoCA.retraso=retraso
        nuevoCA.retraso_tiempo=retraso_tiempo
        nuevoCA.retraso_justificado=retraso_justificado
        nuevoCA.id_alumno=idAlumno
        nuevoCA.id_profesor=idProfesor
        nuevoCA.id_clase=idClase
        nuevoCA.id_asignatura=idASignatura

        #Se guarda en el data store
        nuevoCA_clave = nuevoCA.put()

        #Info de seguimiento
        if v:
            print libName
            print " Return de insertarControlAsistencia: "+str(nuevoCA_clave)+'\n'

        return nuevoCA_clave



    @classmethod
    def insertarResumenControlAsistencia(listaIdCA,fechaHora,idProfesor,idASignatura,idClase):
        pass

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
