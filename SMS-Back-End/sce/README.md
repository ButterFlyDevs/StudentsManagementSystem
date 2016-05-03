##SCE MicroService

[![License](http://img.shields.io/:license-mit-blue.svg)](http://doge.mit-license.org)


**Servicio de Control de Estudiantes**, es el encargado de almacenar y realizar la gestión de la información de los informres de asistencia que los profesores realizan en los primeros minutos de cada clase.
El acceso a este servicio se realiza mediante una interfaz REST.

La información es almacenada en una base de datos noSQL , *Highly Scalable NoSQL Database*, en concreto la [Cloud Datastore](https://cloud.google.com/datastore/docs/) de [Google Cloud Platform](https://cloud.google.com/products/), usando la librería [Google Datastore NDB Client Library](https://cloud.google.com/appengine/docs/python/ndb/) que permite a aplicaciones GAE conctarse a la Cloud Datastore.

Cloud Datastore tiene una gran cantidad de [APIs y librerías](https://cloud.google.com/datastore/docs/apis) para clientes dependiendo del lenguaje que estemos usando y si nuestra aplicación está o no en GAE. En nuestro caso si lo está y usamos [Python NDB Client Library](https://cloud.google.com/appengine/docs/python/ndb/) que también está disponible para Go y Java.


![](diagrama.png)
