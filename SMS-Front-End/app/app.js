// app.js
var routerApp = angular.module('routerApp', ['ui.router']);

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
         template:'HomePage'
       })

        /*Definición de VISTAS ANIDADAS, dentro de una vista general que es la de estudiantes se incrustan
        a su derecha todas las subsecciones distintas. Así estudiantes.html define la plantilla general y dentro de
        ella está una sección en la que se cargarán las subpartes estudiantes.<subpartes>
        Ver estudiantes.html.
        En este caso esta vista no tiene controlador porque no la necesita.
        */
        .state('estudiantes', {
            url: '/estudiantes',
            templateUrl: 'estudiantes.html'
        })

        /*
        Vista "main" anidada dentro de la vista estudiantes, con su propio controlador.
        Asi la vista estudiantes-main.html está anidada dentro de estudiantes.html que se incrusta en la sección <div ui-view></div>
        */
        .state('estudiantes.main', {
            url: '/main',
            templateUrl: 'estudiantes-main.html',
        })

        // nested list with custom controller
         .state('estudiantes.list', {
             url: '/list',
             templateUrl: 'estudiantes-lista.html',
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
           templateUrl: 'estudiantes-detalle.html',
           controller: 'ControladorDetallesEstudiante'
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
             templateUrl: 'estudiantes-nuevo.html',
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
          .state('profesores.detalles-estudiante',{
            url: '/detalle/:estudianteID',
            templateUrl: 'profesores-detalle.html',
            controller: 'ControladorDetallesEstudiante'
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



routerApp.controller('ControladorNuevoEstudiante', function ($scope) {
  /*
  Controlador que manejará los datos del formulario enviándolos al servidor.
  */
  $scope.addAlumno = function(){
    //console.log("lamando a addAlumno()");
    console.log($scope.alumno);
    //console.log($scope.alumno.nombre)

    var ROOT = 'http://localhost:8001/_ah/api';
    gapi.client.load('helloworld', 'v1', null, ROOT);

    gapi.client.helloworld.alumnos.insertaralumno({'nombre':$scope.alumno.nombre,'dni':$scope.alumno.dni}).execute(function(resp){
      //Mostramos por consola la respuesta del servidor
      console.log(resp.message);
      $scope.respuesta=resp.message;
      $scope.$apply();
    });

  };


});


routerApp.controller('ControladorDetallesEstudiante', function($scope, $stateParams){

  //Rescatamos el id de la url y la enviamos con el scope a la vista
  //$scope.id = $stateParams.estudianteID;
  $scope.id=$stateParams.estudianteID;

//  document.write("<script src='/app/js/components/datepicker.js'></script>");
//  document.write("<script src='/app/js/components/form-select.js'></script>");

  var ROOT = 'http://localhost:8001/_ah/api';
  gapi.client.load('helloworld', 'v1', null, ROOT);


  //Pedimos al gateway que nos diga todos los profesores que imparten clase a ese alumno.
  gapi.client.helloworld.alumnos.getProfesoresAlumno({'id':$stateParams.estudianteID}).execute(function(resp){
    console.log(resp);
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


  //Implementación de las acciones que se producen cuando el BOTÓN ELIMINAR se pulsa.
  $scope.ButtonClick = function(){
    console.log("Pulsado boton de eliminar")
    var ROOT = 'http://localhost:8001/_ah/api';
    gapi.client.load('helloworld', 'v1', null, ROOT);

    gapi.client.helloworld.greetings.eliminaralumno({'dni':'sf'}).execute(function(resp){
      //Mostramos por consola la respuesta del servidor
      console.log(resp.message);
      $scope.respuesta=resp.message;
      $scope.$apply();
    });
  }


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
