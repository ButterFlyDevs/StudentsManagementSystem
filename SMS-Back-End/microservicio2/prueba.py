#Fichero funcional

import os
from gcloud import storage
import mimetypes


print "Conectando\n"

#Cargamos las credenciales
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'key.json'

#Nos conectamos al projecto.
client = storage.Client(project='1020593262083')

#Nos conectamos al bucket
bucket = client.get_bucket('prueba_butterflydevs')

#Cargamos una imagen:
f = open('profile.jpg', 'rb')
print 'Nombre: ' +  str(f.name)
tipo = mimetypes.MimeTypes().guess_type(f.name)[0]
print 'Tipo: ' +  tipo
print 'Tam: ' + str(os.path.getsize(f.name))

#print f.read()

#Doc in: https://googlecloudplatform.github.io/gcloud-python/0.4.1/storage-blobs.html
#Creamos un blob:
blob = bucket.blob(f.name)

blob.upload_from_string(f.read(), 'image/jpeg')

url = blob.public_url

print url
