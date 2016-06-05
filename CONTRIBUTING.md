
##Contributing Guidelines

#####Acuerdo de sintaxis

#####Issues, ramas y nuevas funcionalidades

#####Ejecución local

Para testear la aplicación es posible ejecutarla al completo en cualquier entorno local, para ello el único requisito previo será haber ejecutado el fichero de requisitos que descarga el SDK de GAE necesario para correr en modo desarrollador algunos de los servicios que la aplicación usa y ejecutar el lanzador **runAll.sh**. En caso de que quiera detenerse la ejecución y volver a lanzarse deberán de matarse los procesos en ejecución del servidor de desarrollo, con `` kill -9 <process PID> ``  por ejemplo.

Si sólo se quiere lanzar la ejeución del BackEnd debe lanzarse el script **runBackEnd-StandAlone.sh**, con el que se lanzan los tres módulos. En este caso la detención del servidor de desarrollo detiene los tres módulos.
