![](sms.png)

![License](http://img.shields.io/badge/license-GPLv3-blue.svg)
![Status](https://img.shields.io/badge/status-pre--alpha-red.svg)
![coverage](https://img.shields.io/badge/coverage-10%25-orange.svg)


**S**tudent **M**anagement **S**ystem en un agilizador de procesos para centros docentes diseñado para mejorar la recolección, gestión y análisis de datos académicos en tiempo real, potenciando y haciendo más fácil la toma de decisiones, análisis de estado y detección de problemas en centros educativos.

####Arquitectura del sistema

El diseño de la aplicación está basado en microservicios, distribuyendo su funcionamiento en distintos nodos que de forma separada cumplen una función concreta e independiente del resto pero contribuyendo a la lógica total de la aplicación.

 Cada uno de estos servicios cuenta con sus propios recursos en la nube y pueden escalar de forma independiente tanto como lo necesiten, pueden ser desarrollados en lenguajes diferentes y tener acceso a servicios distintos o comunes dentro de la red de Google.

El siguiente esquema refleja el diseño general:

![](documentacion/img/GAEApproach.jpg)

Aunque SMS está pensado para correr en **Google App Engine** es fácilmente adaptable a una ejecución local en máquinas privadas con algunas modificiones relativamente simples.

*SMS es un proyecto Open Source que espera estar en producción muy pronto para un conjunto de centros con unas necesidades muy características que son en las que se está enfocando el desarrollo. A pesar de esto la idea es construirlo tan modularizable que sea fácilmente adaptable, extensible y rediseñable para cualquier necesidad específica. *


####¿Cómo contribuir al proyecto?

Si quieres colaborar con el proyecto tan solo tienes que hacer un **fork** del repositorio, realizar cualquier mejora o modificación del código y proponer un **pull-request**.
Pero antes de nada te aconsejamos que leas el fichero CONTRIBUTING.md donde detallamos mejor los detalles.

¿Te animas a participar en el proyecto?

#####Stack Tech
-------------

A continuación la lista de las principales tecnologías que usamos, por el momento, en el desarrollo:

- [Javascript](https://www.javascript.com/)
- [AngularJS](https://angularjs.org/)
- [HTML5](https://www.w3.org/TR/html5/)
- [UIkit](http://getuikit.com/)
- [Python](https://www.python.org/)
- [Flask](http://flask.pocoo.org/)
- [gRPC](http://www.grpc.io/)
- [JSON](http://www.json.org/json-es.html)
- [MySQL](https://www.mysql.com/)
- [Google Cloud Platform](https://cloud.google.com/)
