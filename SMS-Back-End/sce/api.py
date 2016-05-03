# -*- coding: utf-8 -*-

######################################################
## DEFINICIÓN DE LA API REST del MICROSERVICIO SCE  ##
######################################################

from flask import Flask
from flask import abort
from flask import request
import jsonpickle


#Definición del nombre de la aplicación
app = Flask(__name__)

#Activar modo verbose para mensajes por terminal.
v=1
nombreMicroservicio = '\n## Microservicio SCE ##\n'

#Recurso de prueba el estado del servicio.
@app.route('/prueba',methods=['GET'])
def doSomething():
    '''
    Prueba del estado de la API.
    curl -i -X GET localhost:8003/prueba
    '''
    if v:
        print nombreMicroservicio
        print 'Llamando a /prueba GET doSomething() \n'

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
        print 'Llamando a /controlesAsistencia GET getAllControlesAsistencia() \n'

    return 'getAllControlesAsistencia()\n'

@app.route('/controlesAsistencia', methods=['POST'])
def  insertaControlAsistencia():
    '''
    Inserta un control de asitencia
    curl -i -X GET localhost:8003/controlesAsistencia
    '''
    if v:
        print nombreMicroservicio
        print 'Llamando a /controlesAsistencia POST insertaControlAsistencia() \n'

    return 'insertaControlAsistencia()\n'

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
