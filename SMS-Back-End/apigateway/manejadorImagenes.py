from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

import cloudstorage as gcs
from google.appengine.api.images import get_serving_url
#from google.appengine.api import app_identity
import os

class ManejadorImagenes:

    @classmethod
    def CreateFile(self, nombre, datos):
        my_default_retry_params = gcs.RetryParams(initial_delay=0.2, max_delay=5.0, backoff_factor=2, max_retry_period=15)
        gcs.set_default_retry_params(my_default_retry_params)

        bucket_name = os.environ.get('BUCKET_NAME', 'prueba')
        print bucket_name
        bucket = '/' + bucket_name
        filename = bucket + '/' + nombre

        #https://cloud.google.com/appengine/docs/python/googlecloudstorageclient/functions

        write_retry_params = gcs.RetryParams(backoff_factor=1.1)

        gcs_file = gcs.open(filename, 'w', content_type='image/jpeg', options={'x-goog-meta-foo': 'foo', 'x-goog-meta-bar': 'bar'}, retry_params=write_retry_params)
        gcs_file.write(datos)
        gcs_file.close()

        blobstore_filename = '/gs' + filename
        return get_serving_url(blobstore.create_gs_key(blobstore_filename))
