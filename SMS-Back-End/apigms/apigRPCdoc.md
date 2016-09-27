##Especificaciones de funcionamiento:

### /alumnos

URI de la colección alumnos.

- **GET**

  Devuelve una lista simplificada de todos los alumnos registrados en el sistema, incluyendo sólo el nombre completo y el identificador unívoco (DNI).

  ```curl -X GET localhost:8001/_ah/api/helloworld/v1/alumnos```

- **POST**

  Introduce un nuevo alumno en el sistema.

  ```curl  -d "<datos>" -X POST -G localhost:8001/_ah/api/helloworld/v1/alumnos```
