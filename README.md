# Students Management System

SMS es un sistema de gestión basado en una **aplicación web** para centros docentes que agiliza y mejora la administración de estudiantes haciéndola más simple y eficiente.

###Arquitectura del sistema

El diseño de la aplicación está basado en microservicios, distribuyendo su funcionamiento en distintos nodos que de forma separada cumplen una función concreta e independiente del resto. Cada uno de estos servicios cuenta con sus propios recursos en la nube y pueden escalar de forma independiente tanto como lo necesiten, pueden ser desarrollados en lenguajes diferentes y tener acceso a servicios distintos o comunes dentro de la red de Google.

El siguiente esquema refleja el diseño general:

![](documentacion/img/GAEApproach.jpg)

####Ejecución local

Para testear la aplicación es posible ejecutarla al completo en cualquier entorno local, para ello el único requisito previo será haber ejecutado el fichero de requisitos que descarga el SDK de GAE necesario para correr en modo desarrollador algunos de los servicios que la aplicación usa y ejecutar el lanzador **runAll.sh**. En caso de que quiera detenerse la ejecución y volver a lanzarse deberán de matarse los procesos en ejecución del servidor de desarrollo, con ``` kill -9 <process PID> ``  por ejemplo.

Si sólo se quiere lanzar la ejeución del BackEnd debe lanzarse el script **runBackEnd-StandAlone.sh**, con el que se lanzan los tres módulos. En este caso la detención del servidor de desarrollo detiene los tres módulos.

##### Ejecución de test

Los test unitarios se ejecutan con `unittest` y el test de cobertura con `coverage`. Después de ejecutar los tests unitarios, se genera la información de cobertura.

```
sudo apt-get install python-coverage
cd StudentsManagementSystem/SMS-Back-End/microservicio1/APIDB/test
python testUnitario.py
python-coverage run -m unittest discover
python-coverage report -m
```
