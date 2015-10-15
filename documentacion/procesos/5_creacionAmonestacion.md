## #5 Creación de amonestaciones.

1. El profesor abre un parte de amonestación asociado a un estudiante de uno de sus grupos y rellena ciertos campos del formulario.
2. El estudiante debe rellenar otra serie de campos en el mismo terminal que el profesor. *1*
3. El sistema avisa al tutor de la amonestación. *2*
4. El sistema evaluando el perfil de estudiante decide que acciones tomar.





*1* Habrá que implementar un método seguro en el que el profesor pueda dejar el terminal al estudiante sin que este pueda realizar ninguna otra acción que rellenar sus campos. El profesor podrá volver a habilitar el sistema mediante una contraseña que el haya especificado en su panel de control de usuario.


*2* En nigún caso una amonestación representa un aviso directo al padre, excepto que sea una grave o el estudiante haya acumulado 3 de caracter medio, entonces el sistema avisará al padre si o si.
Cuando un estudiante haya acumulado 5, automaticamente se lanza un aviso urgente al jefe de estudios y al tutor.
Queda por arbitrar las acciones a tomar cuando ocurran más posibilidades.
