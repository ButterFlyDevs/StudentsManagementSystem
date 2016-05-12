# -*- coding: utf-8 -*-

######################################################
## DEFINICIÓN DE LA API REST del MICROSERVICIO SCE  ##
######################################################

from flask import Flask
from flask import abort
from flask import request
import jsonpickle
import Estructuras
import datetime
from NDBlib.gestor import Gestor



#from NDBlib import EstrutcutrasNDB.ControlAsistencia


#Definición del nombre de la aplicación
app = Flask(__name__)

#Activar modo verbose para mensajes por terminal.
v=1
nombreMicroservicio = '\n ## Microservicio SCE ##'

def parseBoolean(cadena):
    if cadena=='True' or cadena== '1':
        return True
    if cadena=='False' or cadena == '0':
        return False

#Recurso de prueba el estado del servicio.
@app.route('/prueba',methods=['GET'])
def doSomething():
    '''
    Prueba del estado de la API.
    curl -i -X GET localhost:8003/prueba
    '''
    if v:
        print nombreMicroservicio
        print ' Llamando a /prueba GET doSomething() \n'


    return 'SCE MicroService is RUNING!\n'

#######################################
#   COLECCIÓN Control Asistencia      #
#######################################

@app.route('/controlesAsistencia', methods=['GET'])
def  getAllControlesAsistencia():
    '''
    Devuelve todos los controles de asistencia.
    curl -i -X GET localhost:8003/controlesAsistencia
    '''

    if v:
        print nombreMicroservicio
        print 'Llamando a /controlesAsistencia GET getAllControlesAsistencia()'

    listaCAs=Gestor.obtenerALLCA()
    '''
    for a in listaCAs:
        print a.asistencia
        json = jsonpickle.encode(a)
        print jsonpickle.decode(json)
    '''


    if v:
        print nombreMicroservicio
        print ' Llamando a /controlesAsistencia GET getAllControlesAsistencia()'
        print ' Salida: '
        print str(listaCAs)

    return jsonpickle.encode(listaCAs)


@app.route('/controlesAsistencia', methods=['POST'])
def  insertaControlAsistencia():


    '''
    Inserta un control de asitencia
    curl -d "fecha=05-10-2016-12-30&asistencia=1&uniforme=1&retraso=0&retraso_tiempo=0&retraso_justificado=1&id_alumno=11&id_profesor=22&id_clase=33&id_asignatura=44" -i -X POST localhost:8003/controlesAsistencia
    '''
    if v:
        print nombreMicroservicio
        print ' Llamando a /controlesAsistencia POST insertaControlAsistencia()'
        print " Petición: "
        print request.form


    #Dividimos la fecha en partes usando el separador -
    fecha = request.form['fecha'].split('-')

    print fecha

    #Creamos un objeto datetime con estas divisiones, siguiendo el formato de datetime:

    #Ejemplo: 05/10/09 18:00 ; date = datetime.datetime(2009, 10, 5, 18, 00)
    #                 año        mes      día       hora     minutos
    date = datetime.datetime(int(fecha[2]), int(fecha[1]), int(fecha[0]), int(fecha[3]), int(fecha[4]))

    #Usando el gestor insertamos el objeto en la base de datos, ajustando los datos que nos llegan a los tipos que se esperan.
    clave=Gestor.insertarControlAsistencia(
                                        date,
                                        parseBoolean(request.form['asistencia']),
                                        parseBoolean(request.form['uniforme']),
                                        parseBoolean(request.form['retraso']),
                                        int(request.form['retraso_tiempo']),
                                        parseBoolean(request.form['retraso_justificado']),
                                        int(request.form['id_alumno']),
                                        int(request.form['id_profesor']),
                                        int(request.form['id_clase']),
                                        int(request.form['id_asignatura']),
                                        )


    if v:
        print nombreMicroservicio
        print ' /controlesAsistencia POST insertaControlAsistencia()'
        print ' Return:'+str(clave)+'\n'

    #Devolvemos la clave que ha sido introducida
    return str(clave)




###############################################
#   COLECCIÓN Resumen Control Asistencia      #
###############################################

@app.route('/resumenesControlesAsistencia', methods=['GET'])
def  getAllResumenesControlesAsistencia():
    '''
    Devuelve todos los controles de asistencia.
    curl -i -X GET localhost:8003/resumenesControlesAsistencia
    '''
    if v:
        print nombreMicroservicio
        print 'Llamando a /resumenesControlesAsistencia GET resumenesControlesAsistencia() \n'

    return 'getAllResumenesControlesAsistencia()\n'

@app.route('/resumenesControlesAsistenciaEspecificos', methods=['GET'])
def  getResumenesControlesAsistenciaConParametros():
    '''
    Devuelve todos los controles de asistencia que cumplen los parámetros pasados
    curl -i -X GET localhost:8003/resumenesControlesAsistenciaEspecificos
    '''
    if v:
        print nombreMicroservicio
        print 'Llamando a /resumenesControlesAsistencia GET resumenesControlesAsistencia() \n'
    return 'getResumenesControlesAsistenciaConParametros()\n'







if __name__ == '__main__':
    app.run(debug=True)
