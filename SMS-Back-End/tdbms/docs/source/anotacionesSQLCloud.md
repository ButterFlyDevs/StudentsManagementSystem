La conexión a la instance de SQL Cloud puede realizarse mediante una IP v6 o v4, en caso de ser v6 es gratis pero
el equipo debe poder hacerlo, en este caso no se ha podido y se ha tenido que acceder mediante una v4. Para eso previamente
hay que activar que este tipo de redes puedan conectarse y esto tiene un precio.

Esta conexión puede realizarse así:

 mysql --host=<ipv4> --user=<user> --password

Esta conexión es sin SSL y esto tiene sus problemas, pero para empezar puede servir. Además de esta forma
la conexión puede realizarse mediante una Power Shell online.


La gestión de la instancia y el acceso a todos los datos se realiza desde la consola cloud de google.
