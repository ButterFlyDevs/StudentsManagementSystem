# -*- coding: utf-8 -*-
"""
Wrapper (envoltorio) de la librería **ndb** (que conecta con Cloud Datastore) y **lógica** del microservicio.
"""

from google.appengine.ext.db import Key
from ModelosNDB import *
import datetime
from termcolor import colored
import time

from pytz import timezone
import pytz


#import logging

#Para activar/desactivar el modo verbose para muestra de mensajes.
v = 1
libName='\n ## Gestor NDB ##'

def parseBoolean(cadena):
    """
    Pequeño parseador que convierte string en booleanos  equivalentes.
    :param cadena: Cadena a convertir, puede ser 'True', 1 o '1'
    :type cadena: string
    :returns: booleano equivalente a la cadena introducido
    :rtype: boolean
    """
    if cadena=='True' or cadena== 1 or cadena == '1' :
        return True
    if cadena=='False' or cadena == 0 or cadena == '0' :
        return False

def boolToInt(boolean):
    """
    Pequeño parseador que convierte booleanos en enteros equivalentes.
    :param boolean: Booleano (True o False) que quermos convertir a entero equivalente.
    :type boolean: boolean
    :returns: entero equivalente al booleano introducido
    :rtype: entero
    """
    if boolean == True:
        return 1
    if boolean == False:
        return 0

class Gestor:

    #Métodos relacionados con la petición de controles de asistencia completos o resúmenes. Más usados en la UI.
    #----------------------------------------------------------------------------------------------------------------#

    @classmethod #tested
    def obtenerControlAsistencia(self, id):
        """
        Devuelve el control de asistencia completo asociado al id pasado en caso de existir en el DataStore

        :param id: Identificador del control de asistencia en el DataStore
        :type id: entero
        :returns: Conjunto de datos que conforman un control de asistencia al completo, parecido al conjunto de datos de entrada de
            insertarControlAsistencia pero extendido con los nombres para la visualizacion en la UI.
        :rtype: diccionario

        Ejemplo de salida::

            {"nombreAsignatura": "nombre de la asig", "nombreClase": "nombreEjemplo", "idAsignatura": 44, "nombreProfesor": "profesorNuevo",
             "controles": [{"nombreAlumno": "nombe y Apellidos", "idAlumno": 11, "uniforme": true, "retrasoJustificado": false,
                            "retraso": 0, "retrasoTiempo": 0, "asistencia": 1},
                           {"nombreAlumno": "nombre y Apellidos", "idAlumno": 15, "uniforme": false, "retrasoJustificado": true,
                            "retraso": 1, "retrasoTiempo": 1, "asistencia": 0}],
              "idProfesor": 22, "idClase": 33, "fechaHora": "14-06-2016 15:58"}

        El diccionario de salida es una construcción del gestor usando los datos de un resumen en el que se buscan todos los microcontroles,
        que se añaden y a los que se les buscan sus nombres de referencia para que **se muestren en la UI**.

        """
        #Una vez obtenido la clave del resumen vamos a obtener todas los controles que se realizaron en
        #ese control y para ello lo primero que tenemos que recuperar es la lista de las claves de los controles
        #refiriéndonos con control al control que se hace de un estudiante individual.

        print 'KEY'
        print id
        ###########
        #Convertimos el id recibido en una clave procesable por ndb
        ###########
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

            #Rescatamos la lista de microControles de Asistencia
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
                if (query.count()==1):
                    alumno = query.get()
                    control["nombreAlumno"]=alumno.nombreAlumno
                else:
                    print 'No existe nombre de referencia almacenado para el Alumno '+str(mc.idAlumno)
                    control["nombreAlumno"]="Indefinido"

                listaControles.append(control)


            #Añadimos la lista obtenida al diccionario que vamos a devolver:
            controlAsistencia["microControlesAsistencia"]=listaControles


            #Ademas ahora añadimos los datos comunes al control, como la fecha e ides y nombres de profesor, clase y asignatura.

            #Los ids
            controlAsistencia["idProfesor"] = resumen.idProfesor
            controlAsistencia["idClase"] = resumen.idClase
            controlAsistencia["idAsignatura"] = resumen.idAsignatura

            #Los nombres

            #Profesor
            query = Profesor.query(Profesor.idProfesor==int(resumen.idProfesor))
            if (query.count()==1):
                profesor = query.get()
                controlAsistencia["nombreProfesor"]=profesor.nombreProfesor

            else:
                print 'No existe nombre de referencia almacenado para el Profesor '+str(resumen.idProfesor)
                controlAsistencia["nombreProfesor"]="Indefinido"


            #Clase
            query = Clase.query(Clase.idClase==int(resumen.idClase))
            if (query.count()==1):
                clase = query.get()
                controlAsistencia["nombreClase"]=clase.nombreClase
            else:
                print 'No existe nombre de referencia almacenado para la clase '+str(resumen.idClase)
                controlAsistencia["nombreClase"]="Indefinido"

            #Asignatura
            query = Asignatura.query(Asignatura.idAsignatura==int(resumen.idAsignatura))
            if (query.count()==1):
                asignatura = query.get()
                controlAsistencia["nombreAsignatura"]=asignatura.nombreAsignatura
            else:
                print 'No existe nombre de referencia almacenado para la asignatura '+str(resumen.idAsignatura)
                controlAsistencia["nombreAsignatura"]="Indefinido"



            #Añadimos
            controlAsistencia["fechaHora"] = datetime.datetime.strftime(resumen.fechaHora, "%d-%m-%Y %H:%M")

            #print 'Finally'
            #print controlAsistencia

            #Devolvemos el control de asistencia construido
            #print colored(controlAsistencia, 'green')
            return controlAsistencia

        else:
            return 'Error not found.'

    @classmethod #tested
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

        .. warning::

            Por ahora solo se pueden hacer búsquedas por días completos o por intervalos de estos, **NO POR HORAS** .

            Los *datetime* pasados serán redondeados a días para la búsqueda.

        """
        if v:
            print libName
            print " Llamada a NDBlib.gestor.obtenerResumenesControlAsistencia() "
            print locals()

        #Creamos una lista de resúmenes que vamos a devoler.
        resumenes = []

        #Los pedimos todos
        query = resumenControlAsistencia.query()

        #Vamos aplicando filtros conforme vamosanalizando parámetros

        if idProfesor:
            query = query.filter(resumenControlAsistencia.idProfesor == idProfesor)
        if idAsignatura:
            query = query.filter(resumenControlAsistencia.idAsignatura == idAsignatura)
        if idClase:
            query = query.filter(resumenControlAsistencia.idClase == idClase)

        #Si solo se ha añadido fecha inicial se busca en todo ese día (por ahora no se hacen búsquedas por horas)
        if fechaHoraInicio and not fechaHoraFin:

            #Se redondea la fecha al día en cuestión con la hora 00:00 (ver warning arriba) y se busca entre esa y un día más.
            fechaInicio = datetime.datetime(fechaHoraInicio.year, fechaHoraInicio.month, fechaHoraInicio.day)
            fechaInicioMas1 = fechaInicio + datetime.timedelta(days=1)
            #Solo se coge la fecha y la hora (nada de minutos), porque el usuario no especificará tanto.
            query = query.filter(resumenControlAsistencia.fechaHora >= fechaInicio, resumenControlAsistencia.fechaHora <= fechaInicioMas1)

        #Si se han pasdo las dos fechas se quiere buscar por el intervalo que marcan.
        elif fechaHoraInicio and fechaHoraFin:

            fechaInicio = datetime.datetime(fechaHoraInicio.year, fechaHoraInicio.month, fechaHoraInicio.day)
            fechaFin = datetime.datetime(fechaHoraFin.year, fechaHoraFin.month, fechaHoraFin.day)
            query = query.filter(resumenControlAsistencia.fechaHora >= fechaInicio, resumenControlAsistencia.fechaHora <= fechaHoraFin)


        #Los guaramos todos en una lista
        listaResumenes = query.fetch()

        print listaResumenes

        #Los recorremos todos para añadirles a cada uno los nombres de las entidades básicas que tienen para que se muestren
        #bien para el usuario en la Interfaz de Usuario
        for a in listaResumenes:

            #Creamos un diccionario donde guardaremos toda la información sobre el resumen de control de asistencia
            rca = {}
            #Guardamos id del resumen
            rca["key"]=a.key.id()
            #Convertimos la fecha en algo legible con el formato que queramos
            rca["fechaHora"]=datetime.datetime.strftime(a.fechaHora, "%d-%m-%Y %H:%M")
            rca["idClase"] = a.idClase
            rca["idAsignatura"] = a.idAsignatura
            rca["idProfesor"] = a.idProfesor

            #Ahora tenemos que añadir los nombre de la clase, asignatura y profesor, porque tienen que verse en la IU
            #Clase
            query = Clase.query(Clase.idClase==int(a.idClase))
            if (query.count()==1):
                clase = query.get()
                rca["nombreClase"]=clase.nombreClase
            else:
                print 'No existe nombre de referencia almacenado para la clase '+str(a.idClase)
                rca["nombreClase"]="Indefinido"

            #Asignatura
            query = Asignatura.query(Asignatura.idAsignatura==int(a.idAsignatura))
            if (query.count()==1):
                asignatura = query.get()
                rca["nombreAsignatura"]=asignatura.nombreAsignatura
            else:
                print 'No existe nombre de referencia almacenado para la asignatura '+str(a.idAsignatura)
                rca["nombreAsignatura"]="Indefinido"


            #Profesor
            query = Profesor.query(Profesor.idProfesor==int(a.idProfesor))
            if (query.count()==1):
                profesor = query.get()
                rca["nombreProfesor"]=profesor.nombreProfesor
            else:
                print 'No existe nombre de referencia almacenado para el profesor'+str(a.idProfesor)
                rca["nombreProfesor"]="Indefinido"


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

    #Métodos relacionados con la inserccion y eliminación de un control de asistencia completo.
    #----------------------------------------------------------------------------------------------------------------#

    @classmethod #tested
    def insertarControlAsistencia(self, controlAsistencia):
        """
        Inserta en el sistema un control de asistencia, un conjunto de microControlesAsistencia (que son los controles
        individuales a los alumnos) más datos comunes a todos ellos dentro del mismo control general.


        :param controlAsistencia: diccionario anidad con todos los datos que componen un controlAsistencia completo, *ver ejemplo de entrada*
        :type controlAsistencia: diccionario
        :returns: Diccionario con status y key del control insertado en caso de haber tenido éxito, que en realidad
            es la key de la entidad resumenControlAsistencia, que es una de las partes en las que en la Base de Datos se divide el
            la entidad más abstracta Control Asistencia *(ver ModelosNDB)* .
        :rtype: diccionario

        Ejemplo de entrada::

            {"microControlesAsistencia": [
                {
              	  "asistencia" : 1,
              	  "retraso": 0,
                  "retrasoTiempo" : 0,
                  "retrasoJustificado" : 0,
                  "uniforme" : 1,
                  "idAlumno" : 11
              	},
                {
                  "asistencia" : 0,
              	  "retraso": 1,
                  "retrasoTiempo" : 1,
                  "retrasoJustificado" : 1,
                  "uniforme" : 0,
                  "idAlumno" : 15
              	}
              ],
            "idProfesor" : 22,
            "idClase" : 33,
        	"idAsignatura" : 44
           }

        Ejemplo de salida::

            {'status': 'OK', 'key': 22L}


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
        base =  datetime.datetime.now()
        fechaHora = datetime.datetime.now(pytz.timezone("Europe/Madrid"))

        #fechaHora = fechaHora.strftime('%Y-%m-%d %H:%M:%S')

        fechaHora3 =datetime.datetime(fechaHora.year, fechaHora.month, fechaHora.day, fechaHora.hour, fechaHora.minute, fechaHora.second)
        #print fechaHora3

        if v:
            print 'Datetime usado:'
            print colored(fechaHora3, 'red')

        #Recorremos todos los elementos de la lista de micro controles de asistencia pasados.
        for microControlAsistencia in controlAsistencia['microControlesAsistencia']:
            #Insertamos el microcontrol y guardamos su key en un vector.
            #Usando el método añadimos el microControlAsistencia con el resto de parámetros globlales a todos los de
            #este control como son la fechaHora, el idProfesor, idClase e idAsignatura (se añade a todos para que tengan esos
            #datos y las búsquedas puedan ser óptimas)
            keys.append(Gestor.insertarMicroControlAsistencia(microControlAsistencia,
                                                              fechaHora3,
                                                              controlAsistencia['idProfesor'],
                                                              controlAsistencia['idClase'],
                                                              controlAsistencia['idAsignatura']))


        print 'KEYS'
        print keys
        '''
        Una vez que se han introducido las asistencias en la tabla ControlAsistencia tenemos que crear un resumen
        en la tabla ResumenControlAsistencia y para eso usamos el método insertarResumenControlAsistencia. Para extraer
        los tres últimos parámetros usamos el primer control pasado en la lista.
        '''

        keyResumen=Gestor.insertarResumenControlAsistencia(keys, fechaHora3, controlAsistencia['idProfesor'],
                                                                            controlAsistencia['idAsignatura'],
                                                                            controlAsistencia['idClase'])

        #Creamos un diccionario para la salida
        salida = {}
        if ('key' not in str(type(keyResumen))):
            salida['status']='FAIL'
        else:
            salida['status']='OK'
            salida['key']=keyResumen.id()
        return salida

    @classmethod #tested
    def eliminarControlAsistencia(self, idResumenControlAsistencia):
        """
        Elimina un control de asistencia del sistema. Un CA está modelado como un resumen *tipo ResumenControlAsistencia* y
        una lista de n micron controles *tipo microControlAsistencia* listados dentro del primero. Por tanto cuando se hace
        la eliminación se borra el resumen y todos los microcontroles a los que se hacer referencia dentro.

        :param idResumenControlAsistencia: id del CA que se quiere eliminar
        :type idResumenControlAsistencia: entero *(key.id())*
        :returns: mensaje de estado en diccionario con clave 'status'
        :rtype: diccionario

        Ejemplo de salida::

            {'status': 'OK'}
            {'status': 'FAIL'}

        """

        #El primer paso es ver si existe un resumen con ese id
        key = ndb.Key('resumenControlAsistencia', long(idResumenControlAsistencia));
        query = resumenControlAsistencia.query(resumenControlAsistencia.key == key)

        salida = {}
        if (query.count()==1):
            #Rescatamos el resumen
            resumen = query.get()
            #Rescatamos la lista de los microControles de Asistencia
            listaKeysMCA=resumen.listaMCAs

            microControlesAntes= microControlAsistencia.query().count()
            print 'AQUI'
            print microControlesAntes
            #print len(listaKeysMCA)
            print listaKeysMCA

            for key in listaKeysMCA:
                #Buscamos el microcontrol en la base de datos y lo eliminamos
                print microControlAsistencia.query(microControlAsistencia.key==key).get()
                mc = microControlAsistencia.query(microControlAsistencia.key==key).get()
                print mc.key.delete()
                #(microControlAsistencia.query(microControlAsistencia.key==key).get()).key.delete()
                #print 'Después de borrar'
                #print microControlAsistencia.query(microControlAsistencia.key==key).get()

            time.sleep(1)

            print 'Despues'
            print microControlAsistencia.query().count()

            #Si se han eliminado bien los microControles
            if microControlAsistencia.query().count() == microControlesAntes-len(listaKeysMCA):
                #Pasamos a eliminar el propio resumen
                resumen.key.delete()

                #Si no esperamos no funciona porque parece que delete funciona de fomra asyncrona y el código sigue
                time.sleep(1)

                #Comprobamos que ya no está:
                query2 = resumenControlAsistencia.query(resumenControlAsistencia.key == key)
                if (query.count()==0):
                    salida['status']='OK'
                else:
                    salida['status']='FAIL'
                    salida['info']='Fallo comprobacion eliminacion'
            else:
                salida['status']='FAIL'
                salida['info']='Fallo al eliminar los microcontroles'
        else:
            salida['status']='FAIL'
            salida['info']='Objeto no encontrado'

        return salida

    @classmethod #tested #privated
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

        Ejemplo param.  mControlAsistencia::

            >>> fechaHora = datetime.datetime.now()
            >>> mca={"asistencia" : 1, "retraso": 0, "retrasoTiempo" : 0, "retrasoJustificado" : 0, "uniforme" : 1, "idAlumno" : 11}
            >>> print Gestor.insertarMicroControlAsistencia(mca, fechaHora, 1, 1, 1)
            Key('microControlAsistencia', 5)

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

    @classmethod #tested #privated
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

        Ejemplo de listaMCAs::

            [Key('microControlAsistencia', 6368371348078592), Key('microControlAsistencia', 4960996464525312)]

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

    # Métodos de las entidades de refencia básicas Alumno, Profesor, Clase y Asignatura.
    #----------------------------------------------------------------------------------------------------------------#

    @classmethod #tested
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

    @classmethod #tested
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

    @classmethod #tested
    def eliminarEntidad(self, tipo, idEntidad):
        """
        Elimina una entidad de referencia un tipo básico de la BD Relacional (Alumno, Profesor,
        Asignatura, Clase), guardado en el datastore, que previamente debe existir.

        .. note:

            Borrar una referencia al nombre completo de una entidad no borra nada más.

        :param tipo: tipo del que queremos eliminar una entidad
        :param idEntidad: id de la entidad (independiente del tipo)
        :type tipo: string ('Alumno', 'Profesor', 'Clase', 'Asignatura')
        :type idEntidad: int
        :returns: Mensaje de control
        :rtype: diccionario

        :Ejemplo:

        >>> Gestor.eliminarEntidad('Alumno', 231143)
        {'status' : 'OK'}
        >>> Gestor.eliminarEntidad('Alumno', 224)
        {'status' : 'FAIL', 'info' : 'Alumno con id 224 no existe.'}
        """

        #Info de seguimiento
        if v:
            print libName
            print " Llamada a eliminarEntidad con params: "
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
            try:
                #Extraemos la entidad y la borramos.
                consulta.get().key.delete()
                salida['status']='OK'
            except ValueError, Argument:
                salida['status']='FAIL'
                salida['info']=Argument
        else:
            salida['status']='FAIL'
            salida['info']='Entidad '+tipo+' con id '+str(idEntidad)+' no existe en el sistema.'

        return salida
