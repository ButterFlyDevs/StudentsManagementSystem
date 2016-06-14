# -*- coding: utf-8 -*-
"""
Wrapper (envoltorio) de la librería ndb que conecta con Cloud Datastore y lógica del sistema
"""

from google.appengine.ext.db import Key
from EstructurasNDB import *
import datetime

#import logging

#Para activar/desactivar el modo verbose para muestra de mensajes.
v = 1
libName='\n ## Gestor NDB ##'


def parseBoolean(cadena):
    if cadena=='True' or cadena== 1 or cadena == '1' :
        return True
    if cadena=='False' or cadena == 0 or cadena == '0' :
        return False

def boolToInt(boolean):
    if boolean == True:
        return 1
    if boolean == False:
        return 0

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

    #Métodos relacionados con la petición de controles de asistencia completos o resúmenes.
    #----------------------------------------------------------------------------------------------------------------#

    @classmethod
    def obtenerControlAsistencia(self, id):
        """
        Devuelve el control de asistencia completo asociado al id pasado en caso de existir en el DataStore

        :param id: Identificador del control de asistencia en el DataStore
        :type id: entero
        :returns: Conjunto de datos que conforman un control de asistencia al completo
        :rtype: diccionario

        Ejemplo de salida::

            {"nombreAsignatura": "nombre de la asig", "nombreClase": "nombreEjemplo", "idAsignatura": 44, "nombreProfesor": "profesorNuevo",
             "controles": [{"nombreAlumno": "nombe y Apellidos", "idAlumno": 11, "uniforme": true, "retrasoJustificado": false,
                            "retraso": 0, "retrasoTiempo": 0, "asistencia": 1},
                           {"nombreAlumno": "nombre y Apellidos", "idAlumno": 15, "uniforme": false, "retrasoJustificado": true,
                            "retraso": 1, "retrasoTiempo": 1, "asistencia": 0}],
              "idProfesor": 22, "idClase": 33, "fechaHora": "14-06-2016 15:58"}

        """
        #Una vez obtenido la clave del resumen vamos a obtener todas los controles que se realizaron en
        #ese control y para ello lo primero que tenemos que recuperar es la lista de las claves de los controles
        #refiriéndonos con control al control que se hace de un estudiante individual.

        print 'KEY'
        print id
        #Convertimos el id recibido en una clave procesable por ndb
        key = ndb.Key('resumenControlAsistencia', long(id));
        print key

        #Extraemos del DataStore la entidad resumenControlAsistencia por el id que nos pasan.
        query = resumenControlAsistencia.query(resumenControlAsistencia.key == key)

        print '\n PROCESO OBTENCIÓN CONTROL ASISTENCIA '


        #Diccionario, objeto principal que vamos a devolver:

        controlAsistencia = {}

        #Comprobamos cuantos resultados hemos obtenido.
        #https://cloud.google.com/appengine/docs/python/ndb/queryclass#Query_count
        #Si se ha encontrado un control con ese id
        if (query.count()==1):
            #Rescatamos el resumen
            resumen = query.get()

            print 'RESUMEN'
            print str(resumen)

            #Una vez recuperado el resumen tendremos que componer una lista donde cada elemento será el control de un
            #estudiante en concreto al que llegaremos gracias a que resumen tiene sus claves almacenadas.

            #Rescatamos la lista de Controles de Asistencia
            listaKeysMCA=resumen.listaMCAs

            #Un objeto Control de Asistencia como el que vamos a devolver tiene una lista de microcontroles (los controles de los estudiantes individuales)
            listaControles = []

            #Recorremos la lista de claves de MCAs y vamos extrayendo con estas claves cada uno de la base de datos.
            for key in listaKeysMCA:
                #Buscamos el microcontrol en la base de datos.
                query = microControlAsistencia.query(microControlAsistencia.key==key)
                #mc=mcontrol=microcontrol
                mc=query.get()
                print 'microcontrol leido'
                print mc

                #Creamos un pequeño diccionario donde guardar los datos leidos.
                control = {}

                #Llenamos los campos del dict con lo que nos interesa
                control["asistencia"]=boolToInt(mc.asistencia)
                control["retraso"]=mc.retraso
                control["retrasoJustificado"]=mc.retrasoJustificado
                control["retrasoTiempo"]=mc.retrasoTiempo
                control["uniforme"]=mc.uniforme
                control["idAlumno"]=mc.idAlumno

                #Además tb queremos añadir su nombre para que se vea en la interfaz
                query = Alumno.query(Alumno.idAlumno==int(mc.idAlumno))
                alumno = query.get()
                control["nombreAlumno"]=alumno.nombreAlumno

                listaControles.append(control)
                print 'Objeto control creado'
                print control


            #Añadimos la lista obtenida al diccionario que vamos a devolver:
            controlAsistencia["controles"]=listaControles

            #Ademas ahora añadimos los datos comunes al control, como la fecha e ides y nombres de profesor, clase y asignatura.

            #Los ids
            controlAsistencia["idProfesor"] = resumen.idProfesor
            controlAsistencia["idClase"] = resumen.idClase
            controlAsistencia["idAsignatura"] = resumen.idAsignatura

            #Los nombres

            #Profesor
            query = Profesor.query(Profesor.idProfesor==int(resumen.idProfesor))
            profesor = query.get()
            controlAsistencia["nombreProfesor"]=profesor.nombreProfesor

            #Clase
            query = Clase.query(Clase.idClase==int(resumen.idClase))
            clase = query.get()
            controlAsistencia["nombreClase"]=clase.nombreClase

            #Asignatura
            query = Asignatura.query(Asignatura.idAsignatura==int(resumen.idAsignatura))
            asignatura = query.get()
            controlAsistencia["nombreAsignatura"]=asignatura.nombreAsignatura


            #Añadimos
            controlAsistencia["fechaHora"] = datetime.datetime.strftime(resumen.fechaHora, "%d-%m-%Y %H:%M")

            print 'Finally'
            print controlAsistencia

            #Devolvemos el control de asistencia construido
            return controlAsistencia

        else:
            return 'Error not found.'

    @classmethod #En el caso de que no se pasara ningún parámetro se buscan todos
    def obtenerResumenesControlAsistencia(self, idProfesor=None, idAsignatura=None, idClase=None, fechaHoraInicio=None, fechaHoraFin=None):
        """
        Se trata de un buscador de resúmenes de controles de asistencia, a continuación rca, configurable por parámetros.

        Cada valor pasado añade una condición a la búsqueda. Si se pasa el parámetro idProfesor se buscarán los
        rcas asociados a ese profesor, pero si además de añade idAsignatura entonces la busqueda se hace bajo esos dos criterios.
        La fecha puede ser solo una, usando `fechaHoraInicio` o un intervalo de tiempo usando `fechaHoraInicio` y `fechaHoraFin`.

        Ahora mismo solo analiza por el profesor

        :param idProfesor: identificador del profesor por el que buscar los rcas.
        :param idAsignatura: identificador de la asignatura por la que buscar los rcas.
        :param idClase: identificador de la clase por el que buscar los rcas.
        :param fechaHoraInicio: Fecha y hora exacta por la que se buscan rcas o inicio de un rango de fecha
        :param fechaHoraFin: Fecha y hora fin del rango con el que opcionalmente se puede buscar
        :type idProfesor: diccionario
        :type idAsignatura: entero
        :type idClase: entero
        :type fechaHora: datetime
        :type fechaHora: datetime
        :returns: Lista de diccionarios donde cada uno es un resumen de un control de asistencia extendido.
        :rtype: lista de diccionarios


        Ejemplo de salida::

            [{"idAsignatura": 44, "idClase": 33, "nombreClase": "mat", "idProfesor": 22, "nombreProfesor": "nombreProfe", "key": 4996180836614144, "fechaHora": "14-06-2016 15:58", "nombreAsignatura": "nombreAsig"},
             {"idAsignatura": 44, "idClase": 33, "nombreClase": "mat", "idProfesor": 22, "nombreProfesor": "nombreProfe", "key": 5101733952880640, "fechaHora": "14-06-2016 16:07", "nombreAsignatura": "nombreAsig"},
             {"idAsignatura": 44, "idClase": 33, "nombreClase": "mat", "idProfesor": 22, "nombreProfesor": "nombreProfe", "key": 5840605766746112, "fechaHora": "14-06-2016 15:48", "nombreAsignatura": "nombreAsig"},
             {"idAsignatura": 44, "idClase": 33, "nombreClase": "mat", "idProfesor": 22, "nombreProfesor": "nombreProfe", "key": 6685030696878080, "fechaHora": "14-06-2016 16:06", "nombreAsignatura": "nombreAsig"}]

        """
        if v:
            print libName
            print " Llamada a NDBlib.gestor.obtenerResumenesControlAsistencia() "
            print locals()

        #Creamos una lista de resúmenes que vamos a devoler.
        resumenes = []

        #BUSQUEDA ACTUALMENTE SOLO HABILITADA POR PROFESOR

        if (idProfesor!=None):
            #Formamos la query
            query = resumenControlAsistencia.query(resumenControlAsistencia.idProfesor == int(idProfesor))
            #Ejecutamos la query en NDB, y por cada elemento creamos un objeto RCA y le volcamos los datos.
            for a in query:

                #Creamos un diccionario donde guardaremos toda la información sobre el resumen de control de asistencia
                rca = {}
                #Guardamos id del resumen
                rca["key"]=a.key.id()
                #Convertimos la fecha en algo legible con el formato que queramos
                rca["fechaHora"]=datetime.datetime.strftime(a.fechaHora, "%d-%m-%Y %H:%M")
                rca["idClase"] = a.idClase
                rca["idAsignatura"] = a.idAsignatura
                rca["idProfesor"] = a.idProfesor

                #Ahora tenemos que añadir los nombre de la clase, asignatura y profesor, porque tienen que verse en la IU.

                #Clase
                query = Clase.query(Clase.idClase==int(a.idClase))
                if (query.count()==1):
                    clase = query.get()
                    rca["nombreClase"]=clase.nombreClase
                else:
                    print 'No existe nombre de referencia almacenado para la clase '+str(clase.idClase)
                    rca["nombreClase"]="Indefinido"

                #Asignatura
                query = Asignatura.query(Asignatura.idAsignatura==int(a.idAsignatura))
                asignatura = query.get()
                rca["nombreAsignatura"]=asignatura.nombreAsignatura

                #Profesor
                query = Profesor.query(Profesor.idProfesor==int(a.idProfesor))
                profesor = query.get()
                rca["nombreProfesor"]=profesor.nombreProfesor

                #Con esto queda el objeto preparado para devolverlo al APIG

                #print 'RCA parseado'
                # Para ver todos los atributos de un objeto con sus valores podemos implementar la función __str__ o usar __dict__
                # print rca.__dict__


                #Lo añadimos a la lista
                resumenes.append(rca)


        if v:
            print libName
            print " Return obtenerResumenesControlAsistencia "
            """
            for r in resumenes:
                #print 'KEY'
                #print r.__str__
                #print r.__dict__
            """

        #Devolvemos la lista, tenga 0, 1 o n elementos.
        return resumenes

    #Métodos relacionados con la inserccion de un control de asistencia completo.
    #----------------------------------------------------------------------------------------------------------------#

    @classmethod
    def insertarControlAsistencia(self, controlAsistencia):
        """
        Inserta en el sistema un control de asistencia, un conjunto de microControlesAsistencia (que son los controles
        individuales a los alumnos) más datos comunes a todos ellos dentro del mismo control general.

        Recibimos un json  con todos los microControlesAsistencia realizados en un ControlAsistencia

        Ejemplo de entrada::

            {"microControlesAsistencia": [
                {
              	  "asistencia" : 1,
              	  "retraso": 0,
                  "retraso_tiempo" : 0,
                  "retraso_justificado" : 0,
                  "uniforme" : 1,
                  "id_alumno" : 11
              	},
                {
                  "asistencia" : 0,
              	  "retraso": 1,
                  "retraso_tiempo" : 1,
                  "retraso_justificado" : 1,
                  "uniforme" : 0,
                  "id_alumno" : 15
              	}
              ],
            "id_profesor" : 22,
            "id_clase" : 33,
        	"id_asignatura" : 44
           }

        .. note::

            La fecha no se inserta para evitar dependencias del sistema del usuario y por eso se calcula en el interior de
            esta función.


        """

        if v:
            print libName
            print " Llamada a insertarControlAsistencia "
            print locals()

        #Creamos una lista donde guardaremos las keys que la base de datos nos devuelva al guardar los controles.
        keys = []

        #Establecemos el datetime para usar el mismo en todas las asistencias al guardarlas, cogiéndolo del sistema.
        fechaHora = datetime.datetime.now()
        if v:
            print 'Datetime usado:'
            print fechaHora

        #Recorremos todos los elementos de la lista de micro controles de asistencia pasados.
        for microControlAsistencia in controlAsistencia['microControlesAsistencia']:
            #Insertamos el microcontrol y guardamos su key en un vector.
            #Usando el método añadimos el microControlAsistencia con el resto de parámetros globlales a todos los de
            #este control como son la fechaHora, el idProfesor, idClase e idAsignatura
            keys.append(Gestor.insertarMicroControlAsistencia(microControlAsistencia,
                                                              fechaHora,
                                                              controlAsistencia['idProfesor'],
                                                              controlAsistencia['idClase'],
                                                              controlAsistencia['idAsignatura']))

        '''
        Una vez que se han introducido las asistencias en la tabla ControlAsistencia tenemos que crear un resumen
        en la tabla ResumenControlAsistencia y para eso usamos el método insertarResumenControlAsistencia. Para extraer
        los tres últimos parámetros usamos el primer control pasado en la lista.
        '''

        keyResumen=Gestor.insertarResumenControlAsistencia(keys, fechaHora, controlAsistencia['idProfesor'],
                                                                            controlAsistencia['idAsignatura'],
                                                                            controlAsistencia['idClase'])

        return 'OK'

    @classmethod
    def insertarMicroControlAsistencia(self, mControlAsistencia, fechaHora, idProfesor, idClase, idAsignatura):
        """
        Inserta una entidad microControlAsistencia en la tabla microControlAsistencia del datastore.

        :param mControlAsistencia: diccionario con el conunto de claves : valor que representa un micro control de asistencia
        :param fechaHora: fecha y hora a la que se registra el micro control
        :param idProfesor: identificador del profesor que realiza el control
        :param idClase: identificador de la clase a la que se le realiza el control
        :param idAsignatura: identificador de la asignatura en la que se está haciendo el control
        :type mControlAsistencia: diccionario
        :type fechaHora: datetime
        :type idProfesor: entero
        :type idClase: entero
        :type idAsignatura: entero
        :returns: La key de la entidad microControlAsistencia introducida en el DataStore
        :rtype: ndb.key

        """

        #Info de seguimiento
        if v:
            print libName
            print " Llamada a insertarMicroControlAsistencia con params: "
            print locals()
            print '\n'

        #Se crea una instancia del modelo DataStore
        mca = microControlAsistencia(fechaHora=fechaHora,
                                     idProfesor=idProfesor,
                                     idAsignatura=idAsignatura,
                                     idClase=idClase,
                                     #El resto de datos vienen en un dict
                                     idAlumno=mControlAsistencia['idAlumno'],
                                     asistencia=parseBoolean(mControlAsistencia['asistencia']),
                                     uniforme=parseBoolean(mControlAsistencia['uniforme']),
                                     retraso=mControlAsistencia['retraso'],
                                     retrasoTiempo=mControlAsistencia['retrasoTiempo'],
                                     retrasoJustificado=parseBoolean(mControlAsistencia['retrasoJustificado'])
                                    )
        #Se guarda en el data store
        claveMca = mca.put()

        #Info de seguimiento
        if v:
            print libName
            print " Return de insertarControlAsistencia: "+str(claveMca)+'\n'

        return claveMca

    @classmethod
    def insertarResumenControlAsistencia(self, listaMCAs, fechaHora, idProfesor, idAsignatura, idClase):

        """
        Inserta una entidad resumenControlAsistencia en la tabla resumenControlAsistencia del datastore, que representa
        el resumen de un control de asistencia realizado, que contiene además de los identificadores de fecha y hora, profesor,
        clase y asignatura donde se realizó la lista de los microcontroles (los controles de cada alumno).

        :param listaMCAs: lista con las keys de las entidades de tipo microControlAsistencia previamente guardadas en el DataStore
        :param fechaHora: fecha y hora a la que se registra el micro control
        :param idProfesor: identificador del profesor que realiza el control
        :param idClase: identificador de la clase a la que se le realiza el control
        :param idAsignatura: identificador de la asignatura en la que se está haciendo el control
        :type listaMCAs: lista
        :type fechaHora: datetime
        :type idProfesor: entero
        :type idClase: entero
        :type idAsignatura: entero
        :returns: La key de la entidad resumenControlAsistencia introducida en el DataStore
        :rtype: ndb.key

        """

        #Info de seguimiento
        if v:
            print libName
            print " Llamada a insertarResumenControlAsistencia con params: "
            print locals()
            print '\n'

        rca = resumenControlAsistencia(listaMCAs=listaMCAs,
                                       fechaHora=fechaHora,
                                       idProfesor=idProfesor,
                                       idAsignatura=idAsignatura,
                                       idClase=idClase)

        #Se guarda en el data store
        rcaClave = rca.put()

        #Info de seguimiento
        if v:
            print libName
            print " Return de insertarResumenControlAsistencia: "+str(rcaClave)+'\n'

        return rcaClave

    # Métodos de las entidades de refencia básicas Alumno, Profesor, Clase y Asignatura
    #----------------------------------------------------------------------------------------------------------------#

    @classmethod
    def insertarEntidad(self, tipo, idEntidad, nombreEntidad):
        """
        Inserta una entidad en cualquiera de los "tipos" de nuestro modelo en el datastore.

        :param tipo: tipo en el que queremos hacer una insercción de una entidad
        :param idEntidad: id con la que se quiere guardar la entidad en la tabla de su tipo (no es la clave en el datastore)
        :param nombreEntidad: nombre completo de la entidad
        :type tipo: string ('Alumno', 'Profesor', 'Clase', 'Asignatura')
        :type idEntidad: int
        :type nombreEntidad: string
        :returns: Mensaje de control
        :rtype: diccionario

        :Ejemplo:

        >>> Gestor.insertarEntidad('Alumno', 231143, 'nombreEjemplo')
        {'status' : 'OK'}
        >>> Gestor.insertarEntidad('Alumno', 231143, 'otroNombre')
        {'status' : 'FAIL', 'info' : 'Alumno con id 231143 ya existe.'}
        >>> Gestor.insertarEntidad('Profesor', 231143, 'nombrePrueba')
        {'status' : 'OK'}

        """

        #Info de seguimiento
        if v:
            print libName
            print " Llamada a insertarEntidad con params: "
            print locals()
            print '\n'

        salida = {}

        #Comprobamos si existe la entidad con ese id en el tipo pasado.
        consulta = None
        if (tipo == 'Alumno'):
            consulta = Alumno.query(Alumno.idAlumno == idEntidad)
        elif (tipo == 'Profesor'):
            consulta = Profesor.query(Profesor.idProfesor == idEntidad)
        elif (tipo == 'Clase'):
            consulta = Clase.query(Clase.idClase == idEntidad)
        elif (tipo == 'Asignatura'):
            consulta = Asignatura.query(Asignatura.idAsignatura == idEntidad)

        #Si existe, salimos informando:
        if (consulta.count() == 1):
            salida['status']='FAIL'
            salida['info']='Entidad '+tipo+' con id '+str(idEntidad)+' ya existe.'

        #Si no existe, lo introducimos:
        else:
            #Creamos la entidad dependiendo del tipo
            entidad = None
            if (tipo == 'Alumno'):
                entidad = Alumno(idAlumno=int(idEntidad), nombreAlumno=nombreEntidad)
            elif (tipo == 'Profesor'):
                entidad = Profesor(idProfesor=int(idEntidad), nombreProfesor=nombreEntidad)
            elif (tipo == 'Clase'):
                entidad = Clase(idClase=int(idEntidad), nombreClase=nombreEntidad)
            elif (tipo == 'Asignatura'):
                entidad = Asignatura(idAsignatura=int(idEntidad), nombreAsignatura=nombreEntidad)

            #La insertamos
            try:
                clave = entidad.put()
                salida['status']='OK'
            except ValueError, Argument:
                salida['status']='FAIL'
                salida['info']=Argument

            #Info de seguimiento
            if v:
                print libName
                print " Return de insertarEntidad: "+str(clave)+'\n'

        return salida

    @classmethod
    def modificarEntidad(self, tipo, idEntidad, nombreEntidad):
        """
        Modifica el nombre de una entidad de un tipo guardado en el datastore, que previamente
        debe existir.

        :param tipo: tipo del que queremos hacer la modificación
        :param idEntidad: id de la entidad (independiente del tipo)
        :param nombreEntidad: nuevo nombre para la entidad
        :type tipo: string ('Alumno', 'Profesor', 'Clase', 'Asignatura')
        :type idEntidad: int
        :type nombreEntidad: string
        :returns: Mensaje de control
        :rtype: diccionario

        :Ejemplo:

        >>> Gestor.modificarEntidad('Alumno', 231143,'nombreEjemplo')
        {'status' : 'OK'}
        >>> Gestor.modificarEntidad('Alumno', 224,'nombreEjemplo')
        {'status' : 'FAIL', 'info' : 'Alumno con id 224 no existe.'}
        """

        #Info de seguimiento
        if v:
            print libName
            print " Llamada a modificarEntidad con params: "
            print locals()
            print '\n'

        salida = {}

        #Comprobamos si existe la entidad del tipo pasado con el id pasado.
        consulta = None
        if (tipo == 'Alumno'):
            consulta = Alumno.query(Alumno.idAlumno == idEntidad)
        elif (tipo == 'Profesor'):
            consulta = Profesor.query(Profesor.idProfesor == idEntidad)
        elif (tipo == 'Clase'):
            consulta = Clase.query(Clase.idClase == idEntidad)
        elif (tipo == 'Asignatura'):
            consulta = Asignatura.query(Asignatura.idAsignatura == idEntidad)


        if (consulta.count() == 1):
            #Extraemos la entidad
            entidad = consulta.get()
            #Dependiendo del tipo modificamos
            if(tipo == 'Alumno'):
                entidad.nombreAlumno = nombreEntidad
            if(tipo == 'Profesor'):
                entidad.nombreProfesor = nombreEntidad
            if(tipo == 'Clase'):
                entidad.nombreClase = nombreEntidad
            if(tipo == 'Asignatura'):
                entidad.nombreAsignatura = nombreEntidad
            try:
                entidad.put()
                salida['status']='OK'
            except ValueError, Argument:
                salida['status']='FAIL'
                salida['info']=Argument
        else:
            salida['status']='FAIL'
            salida['info']='Entidad '+tipo+' con id '+str(idEntidad)+' no existe en el sistema.'

        return salida
