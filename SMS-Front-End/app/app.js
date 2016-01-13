// app.js
var routerApp = angular.module('routerApp', ['ui.router']);

routerApp.config(function($stateProvider, $urlRouterProvider) {

    $urlRouterProvider.otherwise('/home');

    $stateProvider

       .state('#',{
         url:'/',
         template:'HomePage'
       })


        // HOME STATES AND NESTED VIEWS ========================================
        .state('estudiantes', {
            url: '/estudiantes',
            templateUrl: 'estudiantes.html'
        })

        .state('estudiantes.main', {
            url: '/main',
            templateUrl: 'partial-home-main.html',
        })

              // nested list with custom controller
         .state('estudiantes.list', {
             url: '/list',
             templateUrl: 'estudiantes-lista.html',
             controller: 'ControladorEjemplo'
             /*
             controller: function($scope) {
                 $scope.dogs = ['Bernese', 'Husky', 'Goldendoodle'];
             }
             */
         })

         // nested list with just some random string data
         .state('estudiantes.paragraph', {
             url: '/paragraph',
             //Podemos meter directamente texto desde aquí
             template: 'I could sure use a drink right now.'
         })

        // ABOUT PAGE AND MULTIPLE NAMED VIEWS =================================
        .state('about', {
            // we'll get to this in a bit
            url:'/about',
            template: 'This is an another page'
        });

});


routerApp.controller('ControladorEjemplo', function ($scope) {


    console.log("holla");

    var ROOT = 'http://localhost:8001/_ah/api';
    gapi.client.load('helloworld', 'v1', null, ROOT);

 //service.greetings().listGreeting().execute()
        // Get the list of previous scores

    gapi.client.helloworld.greetings.listGreeting().execute(function(resp) {
      //console.log(resp);
      //console.log("after");
      //console.log(resp.alumnos);

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
