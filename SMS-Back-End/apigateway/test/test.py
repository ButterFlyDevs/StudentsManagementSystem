# -*- coding: utf-8 -*-
"""
Para ejecutar el test sólo hay que hacer:
python test.py, con -v para más detalles.
Covertura:
Para que genere contenido en html python-coverage html

..note:
    Para que este test pueda ejecutarse debe estar activado el servidor de desarrollo.

"""

#Para hacer los tests unitarios de la api.
import unittest
#More about in: https://docs.python.org/2/library/unittest.html#unittest.TestCase.setUp

#Como las respuestas son siempre en json incluimos la librería para decodificarlas y tratarlas.
import jsonpickle

#Para los sleeps
import time
urlBase = 'http://localhost:8001/_ah/api/helloworld/v1'
import requests
import json

from pprint import pprint

#Para usar un endpoint desde python
from googleapiclient.discovery import build


"""
Métodos usados para testear el servicio API Gateway.
Este test se podría hacer accediendo a través de la api rest sobre http o mediante RPC,
en este caso como usamos RPC usamos el descubridor de servicios y llamamos directamente a los métodos.
"""


class API_GATEWAY_TESTS(unittest.TestCase):

    """
    def setUp(self):
        print 'Configuración inicial.'
        api_root = 'http://localhost:8001/_ah/api'
        api = 'helloworld'
        version = 'v1'
        discovery_url = '%s/discovery/v1/apis/%s/%s/rest' % (api_root, api, version)
        #Creamos una var global
        self.service = build(api, version, discoveryServiceUrl=discovery_url, cache=False)
        print self.service.__dict__
        #print repr(self.service)
        #pprint(self.service)
    """

    def test_001_HolaMundo(self):
        test = True
        url     = urlBase+'/holaMundo'
        #Introducir un alumno es correcto:
        res = requests.get(url)
        res = jsonpickle.decode(res.text)
        print res
        assert 'Hola mundo! \n' in res['message']


    def test_002_insertarControlAsistencia(self):

        mca = {
            'asistencia': 1,
            'retraso': 1,
            'retrasoJustificado': 1,
            'retrasoTiempo': 10,
            'uniforme': 1,
            'id': 3
            }

        lista = []
        lista.append(mca)

        datos={'microControlesAsistencia': lista, 'idProfesor': 22, 'idClase': 254, 'idAsignatura': 2384}
        payload=json.dumps(datos)

        url = urlBase+'/controlesAsistencia'

        res = requests.post(url, data=payload)
        print res.text
        #Decodificamos el json que hay dentro del propio json de respuesta del API
        message = jsonpickle.decode(jsonpickle.decode(res.text)['message'])

        print 'RES'
        #print res['message']
        #message=jsonpickle.decode(res['message'])
        print message['key']


        #Ahora con el mismo key vamos a intentar rescatar el Control de Asistencia que acabamos de insertar
        datos={'id': 4644337115725824}
        payload=json.dumps(datos)
        print payload
        res2 = requests.get(url, params={'id': message['key']})
        print 'res2'
        print res2
        print res2.url

        assert 'OK' in message['status']



if __name__ == '__main__':
    #main()
    unittest.main()
