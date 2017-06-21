Anotaciones relativas al despliegue:

1. Descargar la última versión del SDK de GAE y configurar la cuenta para el proyecto.

Para hacer el despliegue:

gcloud app deploy app.yaml --project sms-front-end

> gcloud app deploy apigms.yaml --project sms-backend


gcloud app deploy apigms/apigms.yaml dbms/dbms.yaml --project sms-back-end

MYSQL 

Después de crear la instancia de MYSQL nos conectamos y creamos nuestra base de datos.