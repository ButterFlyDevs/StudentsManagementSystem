// Create a new module

/*
The module method was used to create a module named myAppModule.
We also captured the returned object (a reference to the module just created) in a variable, also named myAppModule.
You will notice that we also passed an empty array to the module method.
This can be used to pass a list of dependencies; that is, other modules that this module depends upon.
We don’t have any dependencies, so we simply pass an empty array instead.
*/

var myAppModule = angular.module('myAppModule', ['ngRoute']);
// configure the module with a filter
myAppModule.filter('stripDashes', function() {
        return function(txt) {
          // filter code would go here
        };
});

myAppModule.config(function ($routeProvider) {

            // configure the routes
            $routeProvider

                    .when('/', {
                      // route for the home page
                        templateUrl: 'pages/home.html',
                         controller: 'homeController'
                    })
                    .when('/about', {
                      // route for the about page
                        templateUrl: 'pages/about.html',
                         controller: 'aboutController'
                    })
                    .otherwise({
                      // when all else fails
                        templateUrl: 'pages/routeNotFound.html',
                         controller: 'notFoundController'
                    });
        });


        myAppModule.controller('homeController', function ($scope) {
            $scope.message = 'Welcome to my home page!';
        });

        myAppModule.controller('aboutController', function ($scope) {
            $scope.message = 'Find out more about me.';
        });

        myAppModule.controller('notFoundController', function ($scope) {
            $scope.message = 'There seems to be a problem finding the page you wanted';
            $scope.attemptedPath = $location.path();
        });

angular.module('myAppModule').controller('ControladorEjemplo', function ($scope) {

    console.log("holla");

    var ROOT = 'http://localhost:8001/_ah/api';
    gapi.client.load('helloworld', 'v1', null, ROOT);

 //service.greetings().listGreeting().execute()
        // Get the list of previous scores

    gapi.client.helloworld.greetings.listGreeting().execute(function(resp) {
      console.log(resp);
      $scope.APIcall=resp.message;
      //Tenemos que hacer esto para que se aplique scope ya que la llamada a la API está fuera de Angular
      $scope.$apply();
    });

    var empleados = ['Empleado 1', 'Empleado 2', 'Empleado 3', 'Empleado4'];
    $scope.nuestrosEmpleados = empleados;
    //$scope.salidaAPI="adios";
    }
);
