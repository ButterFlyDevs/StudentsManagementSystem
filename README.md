# Students Management System
SMS es un sistema de gestión implementado en una **aplicación web** para centros docentes que agiliza y mejora la administración de estudiantes haciéndola más simple y eficiente.

Creado para correr en la nube de google con **Google App Engine**, hace uso del framework **webapp2** y por tanto la aplicación será implementada en **Python**.

Para probarla sólo es necesario ejecutar run.sh

-----------------------------------------------------------------


##Arquitectura del sistema

El sistema tendrá dos despliegues simultáneos: uno en **Azure**, y otro en **BlueMix**. 
 
 -- En Azure, habrá hasta un máximo de 4 máquinas simultáneas. Una máquina actuará de "FrontEnd", y será la máquina con la que el cliente del sistema contacte. Esta actuará de balanceador, que repartirá la carga entre dos máquinas (aunque las dos máquinas intervendran sólo si el sistema tiene una fuerte demanda en un momento concreto, actuando una sola máquina si el sistema se encuentra en situación de baja demanda.). La cuarta máquina será la que contendrá la base de datos. Se ha optado por este diseño para minimizar al máximo posible el paso de información entre las dos máquinas de producción; ambas se comunicarán con la misma base de datos y no serán necesarias operaciones de sincornización de recursos. 
 
 -- En BlueMix habrá una réplica de la base de datos de Azure, para tener más seguridad de cara a pérdidas de información. En un principio sólo copiará datos.
 

## Herramientas utilizadas

**En la aplicación**
- 	Se usará el framework **webapp2**, usando como lenguaje de programación PYthon
- 	Para el diseño de la aplicación web, se usará como Framework de CSS **UIKit**
- 	Originalmente, se desarrollará en GoogleApEngine, pero realizaremos modificaciones oportunas para poder hacer el despliegue en máquinas que nosotros podamos manejar.
- 	Motor de base de datos **Mongo DB**

**En la estructura**

- Despliegue en Azure de 4 máquinas (Balanceador, Produccion 1, Produccion 2 [puede no existir/ estar apagada si hay poca carga], Base de datos).
- Despliegue en BlueMix para la réplica de la Base de datos
- Nginx para el balanceador
- Ansible para orquestar todas las máquinas

De la aplicación se encargará para su TFG @ juanAFernandez, y de todo el despliegue en GoogleAppEngine. Para el despliegue automático, testeo, configuración, integración continua, etc. en máquinas (virtuales o no) se encargarán @neon520 y @JA-Gonz. 

Concretamente, @neon520 se encargará de la máquina que actuará de base de datos y de la réplica de ésta, mientras que @JA-Gonz se ocupará de la máquina balanceadora (FrontEnd) y las dos máquinas servidoras intermedias. Cada uno hará sus scripts de configuración y aprovisionamiento, despliegue, testeo, etc. de cada máquina de la cuál se está encargando.

Este proyecto se ha elegido por petición por parte de algunos profesores de un sistema capaz de dar apoyo en las labores del profesorado en la etapa de enseñanza primaria, secundaria y bachillerato. Brindará soporte y agilizará las tareas de los docentes en el día a día en las aulas (pudiendose implementar gestiones de partes de incidencias de comportamiento, asistencia a clase, calificaciones, comunicación con los padres e interna entre personal del centro, etc.)

Este proyecto se presentará al Certamen de proyectos de la UGR organizado por la Oficina de Software Libre.
