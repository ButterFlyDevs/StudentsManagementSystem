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
    Inserta un control de asistencia en el sistema. Compuesto por muchos controles a estudiantes para una asignatura en una clase con un
    profesor en una fecha y hora determinadas.


    Debería recibir una lista de controles de asistencia sin fecha ni hora porque se la colocará este microservicio (para evitar múltiples problemas)
    Esta lista de controles se envía en formato JSON

    Prueba del método:
    curl -X POST  -H 'content-type: application/json' -d @pruebaJson.json localhost:8003/controlesAsistencia
    El fichero sigue el estandar JSON, ver pruebaJson.json. Se pueden validar los ficheros en webs como http://jsonlint.com/.

    '''

    print 'yeaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    print request
    print 'yeaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'

    #Extraemos el JSON de la petición.
    json = request.get_json()


    if v:
        print nombreMicroservicio
        print ' Llamando a /controlesAsistencia POST insertaControlAsistencia()'
        print str(len(json['controles'])) +' controles recibidos\n'
        print " Controles: "
        print json
    

    #Llamamos a la función de NDBlib que inserta el conjunto
    status = Gestor.insertarConjuntoControlAsistencia(json['controles'])



    '''

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
    '''


    if v:
        print nombreMicroservicio
        print ' /controlesAsistencia POST insertaControlAsistencia()'
        print ' Return:'+str(status)+'\n'

    #Devolvemos la clave que ha sido introducida
    return str(status)




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
