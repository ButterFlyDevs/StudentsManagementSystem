# -*- coding: utf-8 -*-
from flask import *

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

import cloudstorage as gcs

app = Flask(__name__)

'''
from gcloud import storage
def upload_image_file(file):
    """
    Upload the user-uploaded file to Google Cloud Storage and retrieve its
    publicly-accessible URL.
    """
    if not file:
        return None

    public_url = storage.upload_file(
        file.read(),
        file.filename,
        file.content_type
    )

    current_app.logger.info(
        "Uploaded file %s as %s.", file.filename, public_url)

    return public_url
'''

def CreateFile(filename):
  """Create a GCS file with GCS client lib.

  Args:
    filename: GCS filename.

  Returns:
    The corresponding string blobkey for this GCS file.
  """

  # Create a GCS file with GCS client.
  #with gcs.open(filename, 'w') as f:
    #f.write('abcde\n')


  write_retry_params = gcs.RetryParams(backoff_factor=1.1)
  gcs_file = gcs.open(filename,
                    'w',
                    content_type='text/plain',
                    options={'x-goog-meta-foo': 'foo',
                             'x-goog-meta-bar': 'bar'},
                    retry_params=write_retry_params)

  gcs_file.write('abcde\n')
  gcs_file.write('f'*1024*4 + '\n')
  gcs_file.close()

  # Blobstore API requires extra /gs to distinguish against blobstore files.
  blobstore_filename = '/gs' + filename
  # This blob_key works with blobstore APIs that do not expect a
  # corresponding BlobInfo in datastore.
  return blobstore.create_gs_key(blobstore_filename)

def prueba():
    print "Prueba"

    my_default_retry_params = gcs.RetryParams(initial_delay=0.2,
                                              max_delay=5.0,
                                              backoff_factor=2,
                                              max_retry_period=15)
    gcs.set_default_retry_params(my_default_retry_params)
    from google.appengine.api import app_identity
    import os
    bucket_name = os.environ.get('BUCKET_NAME', 'prueba')
    #bucket_name = 'prueba'
    print bucket_name

    bucket = '/' + bucket_name
    filename = bucket + '/demo-testfile'

    print 'filename: ' + filename

    #https://cloud.google.com/appengine/docs/python/googlecloudstorageclient/functions


    write_retry_params = gcs.RetryParams(backoff_factor=1.1)
    '''
    gcs_file = gcs.open(filename,
                        'w',
                        content_type='text/plain',
                        options={'x-goog-meta-foo': 'foo',
                                 'x-goog-meta-bar': 'bar'},
                        retry_params=write_retry_params)

    gcs_file.write('abcde\n')
    gcs_file.write('f'*1024*4 + '\n')
    gcs_file.close()

    stat = gcs.stat(filename)
    print 'stat: ' + str(stat)
    '''

    blob_key = CreateFile(filename)
    print 'blob_key: ' + str(blob_key)

    '''
     opens an existing object in the Cloud Storage bucket for reading or overwriting,
     or creates a new object, depending on the specified mode
    '''

    f = open('profile.jpg', 'r')
    filename2 = bucket + '/' + str(f.name)
    print 'filename2: '+filename2
    gcs_file2 = gcs.open(filename2,
                        'w',
                        content_type='image/jpeg',
                        options={'x-goog-meta-foo': 'foo',
                                 'x-goog-meta-bar': 'bar'},
                        retry_params=write_retry_params)
    f = open('profile.jpg', 'r')
    gcs_file2.write(f.read())
    gcs_file2.close()

    from google.appengine.api.images import get_serving_url
    urlImagen = get_serving_url('encoded_gs_file:YXBwX2RlZmF1bHRfYnVja2V0L3Byb2ZpbGUuanBn')

    print 'URLImagen: ' + urlImagen

    #Devolvemos la URL de la imagen guardada en el segemento 'bucket' del Cloud Storage
    blobstore_filename2 = '/gs' + filename2
    return get_serving_url(blobstore.create_gs_key(blobstore_filename2))

    #return get_serving_url(blob_key)



@app.route('/',methods=['GET'])
def saludo():
    # curl -i -X GET localhost:8080
    f = open('profile.jpg', 'r')
    jpgdata = f.read()
    return upload_image_file(f)
    #return 'Hola, soy el microservicio2\n'

@app.route('/2',methods=['GET'])
def saludo2():
    # curl -i -X GET localhost:8080
    f = open('profile.jpg', 'r')
    jpgdata = f.read()
    return prueba()+'\n'
    #return 'Hola, soy el microservicio2, metodo2\n'

if __name__ == '__main__':
    app.run(debug=True)
