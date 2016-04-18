# -*- coding: utf-8 -*-
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

import cloudstorage as gcs
from google.appengine.api import app_identity
from google.appengine.ext import blobstore
from google.appengine.api.images import get_serving_url
#from google.appengine.api import app_identity
import os

class ManejadorImagenes:

    @classmethod
    def CreateFile(self, nombre, datos):
        my_default_retry_params = gcs.RetryParams(initial_delay=0.2, max_delay=5.0, backoff_factor=2, max_retry_period=15)
        gcs.set_default_retry_params(my_default_retry_params)

        bucket_name = os.environ.get('BUCKET_NAME', app_identity.get_default_gcs_bucket_name())

        #bucket_name = os.environ.get('BUCKET_NAME', 'prueba')
        #print bucket_name
        #bucket_name = 'prueba'
        bucket = '/' + bucket_name
        filename = bucket + '/' + nombre

        print 'filename: '+filename

        #https://cloud.google.com/appengine/docs/python/googlecloudstorageclient/functions

        write_retry_params = gcs.RetryParams(backoff_factor=1.1)

        gcs_file = gcs.open(filename, 'w', content_type='image/jpeg', options={'x-goog-meta-foo': 'foo', 'x-goog-meta-bar': 'bar'}, retry_params=write_retry_params)
        gcs_file.write(datos)
        gcs_file.close()

        blobstore_filename = '/gs' + filename

        key = blobstore.create_gs_key(blobstore_filename)


        #Devolvemos la url con la que se puede acceder a la imagen obtenida a partir
        return get_serving_url(key)


    @classmethod
    def DeleteFile(self, url):
        '''
        Eliminaremos la imagen a través de la url que tenemos de ella, extrayendo la clave del blob que se encuentra en la última parte.
        '''
        #key = url[30:]
        key = 'YXBwX2RlZmF1bHRfYnVja2V0L3BydWViYS5qcGc='
        print 'url: '+url
        print 'key: '+key

        key2 = '/app_default_bucket/prueba.jpg'
        print 'key2: '+key2

        #Obtengo una lista de todos los fichetros del bucket
        list = gcs.listbucket("/app_default_bucket")

        print '\n\n\n\n'
        for a in list:
            print a
            print a.filename
            print '\n'


        print '\n\n\n\n'

        '''
        try:
            gcs.delete(key2)
        except gcs.NotFoundError:
            pass
        '''

        #salida=gcs.delete(key)



        return 'COOL'
