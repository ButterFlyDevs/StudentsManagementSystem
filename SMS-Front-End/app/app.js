// app.js
var routerApp = angular.module('routerApp', ['ui.router', 'flow']);

// ############# ENRUTADOR #################################### //

routerApp.config(function($stateProvider, $urlRouterProvider) {
/*

Configura el enrutamiento de todas las vistas de la web. Implementa a que URLs
responden que vistas y mediante que controladores. Estos controladores son las FUNCIONES
que piden los datos donde proceda y los cargan en las vistas donde serán usados y vicesversa (se cargan
de la vista y se usan).
*/

    $urlRouterProvider.otherwise('/home');

    $stateProvider

       //Configura la URL principal
       .state('#',{
         url:'/',
         templateUrl:'main.html'
       })

        /*Definición de VISTAS ANIDADAS, dentro de una vista general que es la de estudiantes se incrustan
        a su derecha todas las subsecciones distintas. Así estudiantes.html define la plantilla general y dentro de
        ella está una sección en la que se cargarán las subpartes estudiantes.<subpartes>
        Ver estudiantes.html.
        En este caso esta vista no tiene controlador porque no la necesita.
        */
        .state('estudiantes', {
            url: '/estudiantes',
            templateUrl: 'estudiantes/estudiantes.html'
        })

        /*
        Vista "main" anidada dentro de la vista estudiantes, con su propio controlador.
        Asi la vista estudiantes-main.html está anidada dentro de estudiantes.html que se incrusta en la sección <div ui-view></div>
        */
        .state('estudiantes.main', {
            url: '/main',
            templateUrl: 'estudiantes/estudiantes-main.html',
        })

        // nested list with custom controller
         .state('estudiantes.list', {
             url: '/list',
             templateUrl: 'estudiantes/estudiantes-lista.html',
             controller: 'ControladorListaEstudiantes'
             /*
             controller: function($scope) {
                 $scope.dogs = ['Bernese', 'Husky', 'Goldendoodle'];
             }
             */
         })

         //Vista detalles estudiantes anidada dentro de estudiantes.
         .state('estudiantes.detalles-estudiante',{
           url: '/detalle/:estudianteID',
           templateUrl: 'estudiantes/estudiantes-detalle.html',
           controller: 'ControladorDetallesEstudiante'
         })

         //Vista detalles estudiantes anidada dentro de estudiantes.
         .state('estudiantes.modificacion-estudiante',{
           url: '/modificacion/:estudianteID',
           templateUrl: 'estudiantes/estudiantes-modificacion.html',
           controller: 'ControladorModificacionEstudiante'
         })

         /* El anidamiento de una tercera vista que no usarmos
         //Vista de datos académicos anidada dentro de detalles de estudiantes.
         .state('estudiantes.detalles-estudiante.datos-academicos',{
           url:'/datos-academicos',
           templateUrl: 'estudiantes-detalle-datos-academicos.html',
           coontroller: 'ControladorDetallesEstudiante-DatosAcademicos'
         })*/

         // nested list with just some random string data
         .state('estudiantes.nuevo', {
             url: '/nuevo',
             //Podemos meter directamente texto desde aquí
             //template: 'I could sure use a drink right now.'
             templateUrl: 'estudiantes/estudiantes-nuevo.html',
             controller: 'ControladorNuevoEstudiante'
         })

         .state('profesores', {
             url: '/profesores',
             templateUrl: 'profesores.html'
         })
         .state('profesores.main', {
             url: '/main',
             templateUrl: 'profesores-main.html',
         })
         .state('profesores.list', {
              url: '/list',
              templateUrl: 'profesores-lista.html',
              controller: 'ControladorListaProfesores'
          })
          .state('profesores.detalles-profesor',{
            url: '/detalle/:profesorID',
            templateUrl: 'profesores-detalle.html',
            controller: 'ControladorDetallesProfesor'
          })
          .state('profesores.nuevo', {
              url: '/nuevo',
              //Podemos meter directamente texto desde aquí
              //template: 'I could sure use a drink right now.'
              templateUrl: 'profesores-nuevo.html',
              controller: 'ControladorNuevoProfesor'
          })








        // ABOUT PAGE AND MULTIPLE NAMED VIEWS =================================
        .state('about', {
            // we'll get to this in a bit
            url:'/about',
            template: 'This is an another page'
        });

});


routerApp.config(['flowFactoryProvider', function (flowFactoryProvider) {
  flowFactoryProvider.defaults = {
    target: 'upload.php',
    permanentErrors: [404, 500, 501],
    maxChunkRetries: 1,
    chunkRetryInterval: 5000,
    simultaneousUploads: 4,
    singleFile: true
  };
  flowFactoryProvider.on('catchAll', function (event) {
    console.log('catchAll', arguments);
  });
  }]);

routerApp.controller('ControladorNuevoEstudiante', function ($location, $scope) {
  /*
  Controlador que manejará los datos del formulario enviándolos al servidor.
  */

  var insertado = 0;
  $scope.submitForm = function(formData){


    //Lógica del formulario.

    //Cuando el formulario es válido porque cumple con todas las especificaciones:
    if ($scope.formNuevoAlumno.$valid) {
       console.log('Formulario válido');
       console.log('Se progecede a guardar al alumno en la base de datos.')

       var salidaEjecucion;

       console.log("llamada a addAlumno()")
       console.log($scope.alumno);

       var ROOT = 'http://localhost:8001/_ah/api';
       gapi.client.load('helloworld', 'v1', null, ROOT);

       gapi.client.helloworld.alumnos.insertarAlumno({
         //Aquí especificamos todos los datods del form que queremos que se envíen:
         'nombre':$scope.alumno.nombre,
         'apellidos':$scope.alumno.apellidos,
         'direccion':$scope.alumno.direccion,
         'localidad':$scope.alumno.localidad,
         'provincia':$scope.alumno.provincia,
         'fecha_nacimiento':$scope.alumno.fecha_nacimiento,
         'telefono':$scope.alumno.telefono,
         'dni':$scope.alumno.dni}
       ).execute(function(resp){
         //Mostramos por consola la respuesta del servidor
         salidaEjecucion=resp.message;
         console.log("Respuesta servidor: "+salidaEjecucion);
         console.log(salidaEjecucion);

          if (salidaEjecucion == 'OK'){
            /*
            Para que los notify de UIkit funcionen deben estar cargdos tanto el fichero de estilo como el javascript
            de este componente,   esto lo hcemos en la plantilla (html)
            */
            $.UIkit.notify("Alumno guardado con muchísimo éxito.", {status:'success'});
            insertado=1;
            console.log("Valor insertar DENTRO DE FUNCION: "+insertado);
            $location.path("/estudiantes/main");
          }else{
            $.UIkit.notify("\""+salidaEjecucion+"\"", {status:'warning'});
            insertado=0;
            console.log("Valor insertar DENTRO DE FUNCION: "+insertado);
          }

         $scope.$apply();
       });



     }
     else {
         //if form is not valid set $scope.addContact.submitted to true
         console.log('Formulario inválido');
         clase="uk-class-danger"
         $scope.formNuevoAlumno.submitted=true;
     };



  };
  console.log("Valor insertar: "+insertado);
  if(insertado == 1 ){
   $location.path("/estudiantes/main");
 }

});

routerApp.controller('ControladorModificacionEstudiante', function($location, $scope, $stateParams){

  //Rescatamos el id de la url y la enviamos con el scope a la vista
  //$scope.id = $stateParams.estudianteID;
  $scope.id=$stateParams.estudianteID;


  var ROOT = 'http://localhost:8001/_ah/api';
  gapi.client.load('helloworld', 'v1', null, ROOT);


  //Pedimos al Gateway toda la informaicón del Alumno.
  gapi.client.helloworld.alumnos.getAlumno({'id':$stateParams.estudianteID}).execute(function(resp) {

    console.log("calling getAlumno with id: "+$stateParams.estudianteID);
    console.log(resp);
    $scope.alumno = resp;
    console.log(resp.nombre);
    $scope.$apply();
    /*
    $scope.es=resp.alumno;
    //Tenemos que hacer esto para que se aplique scope ya que la llamada a la API está fuera de Angular
    $scope.$apply();
    */
  });


  $scope.submitForm = function(formData){


    //Lógica del formulario.

    //Cuando el formulario es válido porque cumple con todas las especificaciones:
    if ($scope.formNuevoAlumno.$valid) {
       console.log('Formulario válido');
       console.log('Se progecede a guardar la modificación del alumno en la base de datos.')

       var salidaEjecucion;

       console.log("llamada a modAlumnoCompleto()")
       console.log($scope.alumno);

       var ROOT = 'http://localhost:8001/_ah/api';
       gapi.client.load('helloworld', 'v1', null, ROOT);

       gapi.client.helloworld.alumnos.modAlumnoCompleto({
         //Aquí especificamos todos los datods del form que queremos que se envíen:
         'id':$stateParams.estudianteID,
         'nombre':$scope.alumno.nombre,
         'apellidos':$scope.alumno.apellidos,
         'direccion':$scope.alumno.direccion,
         'localidad':$scope.alumno.localidad,
         'provincia':$scope.alumno.provincia,
         'fecha_nacimiento':$scope.alumno.fecha_nacimiento,
         'telefono':$scope.alumno.telefono,
         'dni':$scope.alumno.dni}
       ).execute(function(resp){
         //Mostramos por consola la respuesta del servidor
         salidaEjecucion=resp.message;
         console.log("Respuesta servidor: "+salidaEjecucion);
         console.log(salidaEjecucion);

          if (salidaEjecucion == 'OK'){
            /*
            Para que los notify de UIkit funcionen deben estar cargdos tanto el fichero de estilo como el javascript
            de este componente, esto lo hcemos en la plantilla (html)
            */
            $.UIkit.notify("Alumno guardado con muchísimo éxito.", {status:'success'});
          }else{
            $.UIkit.notify("\""+salidaEjecucion+"\"", {status:'warning'});
          }

         $scope.$apply();
       });



     }
     else {
         //if form is not valid set $scope.addContact.submitted to true
         console.log('Formulario inválido');
         clase="uk-class-danger"
         $scope.formNuevoAlumno.submitted=true;
     };



  };




});

routerApp.controller('ControladorDetallesEstudiante', function($location, $scope, $stateParams){

  //Implementación de las acciones que se producen cuando el BOTÓN ELIMINAR se pulsa.
  $scope.delAlumno = function(){
    console.log("Pulsada confirmación eliminación alumno id: "+$stateParams.estudianteID)

    var ROOT = 'http://localhost:8001/_ah/api';
    gapi.client.load('helloworld', 'v1', null, ROOT);

    gapi.client.helloworld.alumnos.delAlumno({'id':$stateParams.estudianteID}).execute(function(resp){
      //Mostramos por consola la respuesta del servidor
      console.log(resp.message);
      $scope.respuesta=resp.message;


      //El mensje no sale debido (en principio) a que cambiamos de pantall
      if (resp.message == 'OK'){
        /*
        Para que los notify de UIkit funcionen deben estar cargdos tanto el fichero de estilo como el javascript
        de este componente, esto lo hcemos en la plantilla (html)
        */
        $.UIkit.notify("Alumno eliminado con éxito.", {status:'success'});
      }else{
        $.UIkit.notify("\""+resp.message+"\"", {status:'warning'});
      }


      $scope.$apply();
    });

    //Después volvemos a la página principal de estudiantes, ahora desbloqueado porque se pierde el mensaje al cambiar,
    // al menos que le pasásemos los datos al controlador de esa página y fuese esa quien cargase el mensaje flotante.
    //$location.path("/estudiantes/main");

  };

  //Rescatamos el id de la url y la enviamos con el scope a la vista
  //$scope.id = $stateParams.estudianteID;
  $scope.id=$stateParams.estudianteID;

  console.log("ID estudiante: "+$stateParams.estudianteID);

  var ROOT = 'http://localhost:8001/_ah/api';
  gapi.client.load('helloworld', 'v1', null, ROOT);


  //Pedimos al gateway que nos diga todos los profesores que imparten clase a ese alumno.
  gapi.client.helloworld.alumnos.getProfesoresAlumno({'id':$stateParams.estudianteID}).execute(function(resp){
    console.log("Profesores del alumno: ");
    console.log(resp.profesores);
    //Enviamos al scope no toda la respuesta sino la lista de profesores que se espeara que contenga esta.
    $scope.profesores = resp.profesores;
    $scope.$apply();
  });

  //Pedimos al Gateway toda la informaicón del Alumno.
  gapi.client.helloworld.alumnos.getAlumno({'id':$stateParams.estudianteID}).execute(function(resp) {

    console.log("calling getAlumno with id: "+$stateParams.estudianteID);
    console.log(resp);
    $scope.alumno = resp;
    console.log(resp.nombre);
    $scope.$apply();
    /*
    $scope.es=resp.alumno;
    //Tenemos que hacer esto para que se aplique scope ya que la llamada a la API está fuera de Angular
    $scope.$apply();
    */
  });




});

routerApp.controller('ControladorDetallesEstudiante-DatosAcademicos', function($scope, $stateParams){
  $scope.id=$stateParams.estudianteID;


});

routerApp.controller('ControladorListaEstudiantes', function ($scope) {
  /*
  Controlador que maneja los datos que se muestran en la vista estudiantes-lista.html y que
  realiza la petición de la lista de Estudiantes y que la carga en el $scope bajo la variable "alumnos".
  */

    var ROOT = 'http://localhost:8001/_ah/api';
    gapi.client.load('helloworld', 'v1', null, ROOT);

 //service.greetings().listGreeting().execute()
        // Get the list of previous scores

    gapi.client.helloworld.alumnos.getAlumnos().execute(function(resp) {
      //console.log(resp);
      //console.log("after");
      console.log(resp.alumnos);

      /*Usar los datos que nos proporciona nuestra API es muy sencillo, sólo tenemos que extraer del JSON que se
      encuentra en "resp" los datos que nos interesan. En este caso es un array de alumnos, por tanto
      solo tenemos que hacer resp.alumnos. ¡Ya está! Ya tenemos cargado el array y dentro de este todos los
      items a los que podemos acceder a sus atributos fácilmente.
      */

      $scope.alumnos=resp.alumnos;
      //Tenemos que hacer esto para que se aplique scope ya que la llamada a la API está fuera de Angular
      $scope.$apply();
    });

    var empleados = ['Empleado 1', 'Empleado 2', 'Empleado 3', 'Empleado4'];
    $scope.nuestrosEmpleados = empleados;
    //$scope.salidaAPI="adios";
    }
);


// #################################
// # Controladores de profesores.  #
// #################################
routerApp.controller('ControladorListaProfesores', function ($scope) {
    /*
    Controlador que provee a la plantilla profesores-lista.html la lista simplificada de todos los profesores
    a trabés del API Gateway usando el método getProfesores()
    */
    var ROOT = 'http://localhost:8001/_ah/api';
    gapi.client.load('helloworld', 'v1', null, ROOT);

    gapi.client.helloworld.profesores.getProfesores().execute(function(resp) {
      console.log(resp.profesores);
      $scope.profesores=resp.profesores;
      $scope.$apply();
    });
    }
);

routerApp.controller('ControladorDetallesProfesor', function($location, $scope, $stateParams){

  //Implementación de las acciones que se producen cuando el BOTÓN ELIMINAR se pulsa.
  $scope.delProfesor = function(){
    console.log("Pulsada confirmación eliminación profesor id: "+$stateParams.profesorID)

    var ROOT = 'http://localhost:8001/_ah/api';
    gapi.client.load('helloworld', 'v1', null, ROOT);

    gapi.client.helloworld.profesores.delProfesor({'id':$stateParams.profesorID}).execute(function(resp){
      //Mostramos por consola la respuesta del servidor
      console.log(resp.message);
      $scope.respuesta=resp.message;


      //El mensje no sale debido (en principio) a que cambiamos de pantall
      if (resp.message == 'OK'){
        /*
        Para que los notify de UIkit funcionen deben estar cargdos tanto el fichero de estilo como el javascript
        de este componente, esto lo hcemos en la plantilla (html)
        */
        $.UIkit.notify("Profesor eliminado con éxito.", {status:'success'});
      }else{
        $.UIkit.notify("\""+resp.message+"\"", {status:'warning'});
      }


      $scope.$apply();
    });

    //Después volvemos a la página principal de profesores, ahora desbloqueado porque se pierde el mensaje al cambiar,
    // al menos que le pasásemos los datos al controlador de esa página y fuese esa quien cargase el mensaje flotante.
    //$location.path("/profesores/main");

  };

  //Rescatamos el id de la url y la enviamos con el scope a la vista
  //$scope.id = $stateParams.estudianteID;
  $scope.id=$stateParams.profesorID;
  console.log("ID profesor: "+$stateParams.profesorID);

  var ROOT = 'http://localhost:8001/_ah/api';
  gapi.client.load('helloworld', 'v1', null, ROOT);


  //Pedimos al gateway que nos diga todos los profesores que imparten clase a ese alumno.
  gapi.client.helloworld.alumnos.getProfesoresAlumno({'id':$stateParams.estudianteID}).execute(function(resp){
    console.log("Profesores del alumno: ");
    console.log(resp.profesores);
    //Enviamos al scope no toda la respuesta sino la lista de profesores que se espeara que contenga esta.
    $scope.profesores = resp.profesores;
    $scope.$apply();
  });

  //Pedimos al Gateway toda la informaicón del profesor.
  gapi.client.helloworld.profesores.getProfesor({'id':$stateParams.profesorID}).execute(function(resp) {

    console.log("calling getProfesor with id: "+$stateParams.profesorID);
    console.log(resp);
    $scope.profesor = resp;
    $scope.$apply();

  });

});
