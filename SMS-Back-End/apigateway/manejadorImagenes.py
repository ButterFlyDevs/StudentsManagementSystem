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


        #Devolvemos la url con la que se puede acceder a la imagen obtenida a partir de la key.
        return get_serving_url(key)


    @classmethod
    def DeleteFile(self, url):
        '''
        Eliminaremos la imagen a través de la url que tenemos de ella, extrayendo la clave del blob que se encuentra en la última parte.

        '''


        '''
        Ejemplo de url en el servidor Cloud Storage
        http://lh3.googleusercontent.com/B_Wu0n-9mAiuFtTttGLIEjXsoXj2gFpup_fJ91z44IewODcaY1Adi-cyRc6Yy0MaFL8NfgnOUhyKB_VyL4v0KNg
        Para obtener la key hay que quitar los primeros 33 caracteres.

        Ejemplo de url en el dev-server:
        http://localhost:8001/_ah/img/encoded_gs_file:YXBwX2RlZmF1bHRfYnVja2V0L2pha2UuanBn
        Para obtener la key hay que quitar los primeros 30 caracteres.
        '''


        #Prueba:
        #Si estamos en el servidor de producción eliminamos los 33 primeros caracteres.
        if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
            key = url[33:]
        #Si estamos en el servidor de desarrollo quitamos los 30 primeros caracteres.
        else:
            key = url[30:]


        print 'url: '+url
        print 'key: '+key


        '''
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
            #gcs.delete(key2)
            salida=blobstore.delete(key)
            return 'OK'
        except gcs.NotFoundError:
            return 'FAIL'


    @classmethod
    def DeleteFile2(self, nombreImagen):
        '''
        Eliminaremos la imagen a partir del nombre
        '''
        bucket_name = os.environ.get('BUCKET_NAME', app_identity.get_default_gcs_bucket_name())
        bucket = '/' + bucket_name
        filename = bucket + '/' + nombreImagen
        try:
            salida=gcs.delete(filename)
            return 'OK'
        except gcs.NotFoundError:
            return 'FAIL'
