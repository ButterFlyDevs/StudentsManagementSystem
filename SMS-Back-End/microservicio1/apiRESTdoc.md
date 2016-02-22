##Diseño de identificadores de recursos con URIs,  especificación.

### /alumnos

URI de la colección alumnos.

- **GET**

  Lee todas las entidades de la colección alumnos.
  Usa *getAlumnos()* de la APIDB.

- **PUT**

  Actualización múltiple/masiva de la colección.
  Realiza un procedimiento iterativo que llama a *nuevoAlumno()* de la APIDB.

- **DELETE**

  Elimina todo el contenido de la colección.
  Utiliza *delAlumnos()* de la APIDB.

- **POST**

  Crea una nueva entidad alumno en la colección.
  Usa *nuevoAlumno()* de la APIDB.


### /alumnos/id_alumno

URI de una entidad de la colección, permite el acceso a
una entidad alumno por medio de su identificador y la jerarquía de dominio.

Ejemplo: */alumnos/11223344X*

- **GET**

  Devuelve la información al completo de un alumno. Hace uso de la función *getAlumno()* de la APIDB.

- **PUT**

  Actualiza los datos de un alumno, llamando a *modAlumno()* de la APIDB.

- **DELETE**

  Borra una entidad alumno en concreto de la coleccion, usando *delAlumno()* de la APIDB.

### /alumnos/id_alumno/profesores

URI que ofrece los profesores que imparten clase a un alumno en concreto.

  - **GET**

  Devuelve la lista de profesores, haciendo uso de *getProfesores()* de la APIDB.

### /alumnos/id_alumno/asignaturas

URI que ofrece las asignaturas en las que está matriculado un alumno en concreto.

  - **GET**

  Devuelve la lista de asignaturas, haciendo uso de *getAsignaturas()* de la APIDB.


### /alumnos/id_alumno/cursos
URI que ofrece los cursos en las que está matriculado un alumno en concreto.

  - **GET**

  Devuelve la lista de cursos, haciendo uso de *getCursos()* de la APIDB.


##Uso de curl para testing:

Con curl podemos testear nuestra api de forma muy simple
por terminal.

Por ejemplo:

Para probar un método en concreto de un recurso lo especificamos con **-X**, por ejemplo:

```
curl -X GET localhost:8080/alumnos
curl -X PUT localhost:8080/alumnos
```

Si queremos ver las cabeceras y no sólo el cuerpo del mensaje devuelto usamos **-i**, por ejemplo:

```
curl -i -X GET localhost:8080/algo
HTTP/1.1 200 OK
content-type: text/html; charset=utf-8
Cache-Control: no-cache
Expires: Fri, 01 Jan 1990 00:00:00 GMT
Content-Length: 6
Server: Development/2.0
Date: Sun, 21 Feb 2016 10:12:06 GMT

hello
```
