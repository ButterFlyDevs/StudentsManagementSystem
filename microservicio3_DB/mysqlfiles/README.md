####Contenido

Los ficheros DBCreator_vxx.sql donde xx es la versión del mismo son script de creación del modelo de la base de datos representado por el
diagrama Entidad Relación de la imagen ER_vxx.jpg.  A su vez los ficheros de creación contienen llamadas a los ficheros
addContenido_vxx.sql que provisionan de contenido de prueba a la base de datos creada.

Para ejecutar estos ficheros DBCreator_vxx.sql sólo hay que arrancar MySql así:

`mysql -u root -p < DBCreator_vxx.sql`


Para conocer más detalle sobre la evolución de las versiones de la Base de Datos y su justificación, ver fichero versions.md
