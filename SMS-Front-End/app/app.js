// app.js
function googleOnLoadCallback(){
  console.log('googleOnLoadCallback is calling');
    var apisToLoad = 1; // must match number of calls to gapi.client.load()
    var gCallback = function() {
        if (--apisToLoad == 0) {
            //Manual bootstraping of the application
            var $injector = angular.bootstrap(document, ['routerApp']);
            console.log('Angular bootstrap complete ');
            console.log('Librería gAPI cargada: ');
            console.log(gapi);
        };
    };



    //gapi.client.load('helloWorld', 'v1', gCallback, '//' + window.location.host + '/_ah/api');
    //Cargamos la gAPI de nuestro backend solo una vez para toda la aplicación.
    /*
    Dependiendo de donde estemos se cargará la api desde el local o desde el backend desplegado en GAE.
    */
    var ROOT;

    if(document.location.hostname=="localhost"){
        ROOT = 'http://localhost:8001/_ah/api';
        console.log('Conectando con APIGateway en localhost');
    }else{
        ROOT = 'https://sms-backend.appspot.com/_ah/api';
        console.log('Conectando con APIGateway en sms-backend');
    }
    gapi.client.load('helloworld', 'v1', gCallback, ROOT);



}
function encode_utf8(s) {
  return unescape(encodeURIComponent(s));
};




//Definición de la aplicación:
//https://github.com/angular-ui/ui-router
var routerApp = angular.module('routerApp', ['ui.router' ,'flow']);

//Podemos hacer lo mismo para los roles dentro del sistema:
routerApp.constant('USER_ROLES', {
  all: '*',
  admin: 'admin',
  editor: 'editor',
  guest: 'guest'
});




// #############
// Controlador de Login
// #############
/*
routerApp.run(function ($rootScope, $location, Auth) {
 // Redirect to login if route requires auth and you're not logged in
     $rootScope.$on('$stateChangeStart', function (event, toState, toParams) {
       Auth.isLoggedInAsync(function(loggedIn) {
         if (toState.authenticate && !loggedIn) {
               $rootScope.returnToState = toState.url;
               $rootScope.returnToStateParams = toParams.Id;
               $location.path('/login');
           }
       });
     });
   ]);

*/
/*
routeApp.run(function ($rootScope) {

  $rootScope.$on('$stateChangeStart', function (event, toState, toParams) {
    var requireLogin = toState.data.requireLogin;

    if (requireLogin && typeof $rootScope.currentUser === 'undefined') {
      event.preventDefault();
      // get me a login modal!
    }
  });

});
*/

//Definimos un monton de constantes.
routerApp.constant('AUTH_EVENTS', {
  loginSuccess: 'auth-login-success',
  loginFailed: 'auth-login-failed',
  logoutSuccess: 'auth-logout-success',
  sessionTimeout: 'auth-session-timeout',
  notAuthenticated: 'auth-not-authenticated',
  notAuthorized: 'auth-not-authorized'
});



//Para las sesiones:
routerApp.service('Session', function () {
  this.create = function (sessionId, userId, userRole) {
    console.log('create in service Session');
    console.log('sessionID: '+sessionId);
    console.log('userId: '+userId);
    console.log('userRole: '+userRole);
    this.id = sessionId;
    this.userId = userId;
    this.userRole = userRole;
  };
  this.destroy = function () {
    this.id = null;
    this.userId = null;
    this.userRole = null;
  };
})

//La lógica relacionada con la autentificación y la autorización (control de acceso) es mejor
//agruparla junta en un servicio.

/*
$http es un Service que facilita las comunicaciones con servidores HTTP remotos vía XMLHttpRequest object or via JSONP.
Doc aquí: https://docs.angularjs.org/api/ng/service/$http
*/
routerApp.factory('AuthService', function ($rootScope, $http, Session, AUTH_EVENTS) {
  var authService = {};

  authService.login = function (credentials) {

    console.log('Inside authService.login');

    /*
    Aquí estamos realizando una petición a una url concreta pasándole unos datos concretos
    y devuelve una promesa.
    */
    /*
    return $http
      .post('/login', credentials).then(function (res) {
                                  Session.create(res.data.id, res.data.user.id, res.data.user.role);
                                  return res.data.user;
                                  });
    */
    //Vamos a pasar de la petición al servidor y vamos a hacer que se cree la sesión:

    var p1 = new Promise(function(resolve, reject) {

      //En esta función tenríamos que comprobar que el usuario está en el sistema
      console.log('Checking credentials')
      console.log(credentials.username)
      console.log(credentials.password)




      gapi.client.helloworld.login.loginUser({'username': credentials.username, 'password': credentials.password}).execute(function(resp){
          console.log('Respuesta del servidor');
          console.log(resp);

          if (resp.message != 'Usuario no encontrado'){
            //Construimos el tipo de dato sesionUsuario
            var sesionUsuario = {
              id : '1',
              user :{
                name: resp.nombre,
                id: resp.idUser,
                role: resp.rol
              },
            };

            resolve(sesionUsuario);
          }else{
            console.log('BAD credentials');
            reject ("Error!");
          }

      });


    //  resolve("Success!");
      // or
      // reject ("Error!");
    });

    p1.then(function(value) {
      console.log(value); // Success!
      //Session.create('11387', '1', 'admin');
      Session.create(value.id, value.user.id, value.user.role);
      //el return se pone auqneu parece que no hace nada
      return value.user;
      //return '1';
    //Session.create(res.data.id, res.data.user.id, res.data.user.role);
    //  return res.data.user;
    }, function(reason) {
      console.log(reason); // Error!
    });

    //Session.create('11387', '1', 'admin');
    //return '1';

    return p1;

  };

  //log out the user and broadcast the logoutSuccess event
	authService.logout = function(){

	}

  authService.isAuthenticated = function () {
    return !!Session.userId;
  };

  authService.isAuthorized = function (authorizedRoles) {

    console.log('Inside isAuthorized');
    console.log(authorizedRoles[0]);
    //Doc here: https://docs.angularjs.org/api/ng/function/angular.isArray
    // isArray es una función de Angular que comprueba si lo pasado es o no un array.
    if (!angular.isArray(authorizedRoles)) {
      console.log('Dentro del if');
      authorizedRoles = [authorizedRoles];
    }else{
      console.log('Se trata de un array');
    }
    //Imprimimos por pantalla lo que devolvería:
    console.log(authService.isAuthenticated() && authorizedRoles.indexOf(Session.userRole) !== -1);
    if (authorizedRoles[0] == '*'){
      console.log('Debería estar autorizado');
      return true
    }else{
      return (authService.isAuthenticated() && authorizedRoles.indexOf(Session.userRole) !== -1);
    }
  };

  //Cuando se usa la factoría se usa una instancia de ella misma que es lo que se devuelve aquí
  return authService;
})

//Controlador de la vista de la sección de login
routerApp.controller('LoginController', function ($scope, $rootScope,  AUTH_EVENTS, AuthService, Session) {

  $scope.prueba = function(){
    $.UIkit.notify("prueba", {status:'warning'});
  }

  $scope.login = function (credentials) {

    console.log('Logueando al usuario con credenciales:')
    console.log(credentials);

    /*
    Al llamar a AuthService.login le pasamos las credenciales y en caso de la que la función tenga éxito
    se ejecuta la primera función y en caso de no tener y recibir el mensaje de fallo se ejecuta la segunda función.
    .then devuelve una promesa
    */
    AuthService.login(credentials).then(function (usuario) {
      $rootScope.$broadcast(AUTH_EVENTS.loginSuccess);
      $scope.setCurrentUser(usuario.user);



    //Implementamos una función que defina que hacer en caso de no haber tenido éxito.
    }, function () {
      $rootScope.$broadcast(AUTH_EVENTS.loginFailed);
      //Mostramos un mensaje diciendo que no ha sido encontrado ese usuario.
      $.UIkit.notify("Usuario no encontrado.", {status:'warning'});

      //Y vaciamos los campos.
      $scope.credentials=null;
      $scope.$apply();

    });
  };

  $scope.logout = function (){
    AuthService.logout();
    Session.destroy();
    //$window.sessionStorage.removeItem("userInfo");
    $rootScope.$broadcast(AUTH_EVENTS.logoutSuccess);
    $scope.setCurrentUser(null);
  }


});

routerApp.controller('ApplicationController', function ($scope, $location, USER_ROLES, AuthService) {
  $scope.currentUser = null;
  $scope.userRoles = USER_ROLES;
  $scope.isAuthorized = AuthService.isAuthorized;

  $scope.setCurrentUser = function (user) {
    console.log('Inside setCurrentUser');
    console.log('user in setCurrentUser:');
    console.log(user);
    $scope.currentUser = user;

    //Tras la autenticación del usuario y su seteo como usuario actual llevamos a la ventana principal.
    $location.path("/home");

    $scope.$apply();

  };
});


routerApp.run(function ($rootScope, AUTH_EVENTS, AuthService) {
  $rootScope.$on('$stateChangeStart', function (event, next) {
    console.log('Authorized roles here: ');
    console.log(next.data.authorizedRoles);
    //Extraemos los datos de autorización de la página a la que vamos.
    var authorizedRoles = next.data.authorizedRoles;

    //Comprobamos si le está permitido o no.

    //SI NO ESTÁ PERMITIDO ...

    /*
    Se usa la factoría AuthService, la función isAuthorized a la que se le pasan
    los datos de autorización de la página a la que estamos accediendo.

    En este caso los datos que se están pasando
    Array [ "guest" ]

    */

    if (!AuthService.isAuthorized(authorizedRoles)) {


      event.preventDefault();

      if (AuthService.isAuthenticated()) {
        // user is not allowed
        console.log('Not allowed!!!!!!');
        $rootScope.$broadcast(AUTH_EVENTS.notAuthorized);
      } else {
        // user is not logged in
        console.log('Not logged in !!!!!!!!');
        $rootScope.$broadcast(AUTH_EVENTS.notAuthenticated);
      }

    }
  });
});


// #################################
// # Controladores de asignaturas  #
// #################################

routerApp.controller('ControladorNuevoEstudiante', function ($location, $scope) {
  /*
  Controlador que manejará los datos del formulario enviándolos al servidor.
  */
  function insertarAlumno2ConImagen(e, datos)
  {
    console.log('HOla uploadFile')
    console.log(e)
    console.log(e.files)
    //Llamamos a la función que sube la imagen:
    //subirImagen($scope.file, 'caca');


    angular.forEach(e.files, function(flowFile, i){
       var fileReader = new FileReader();
          var nombre = flowFile.file.name;

          fileReader.onload = function (event) {
            var uri = event.target.result;
              //$scope.imageStrings[i] = uri;

              var res = uri.slice(23);
              //console.log('Sending2 : ' + res);

              //Añadimos la imagen a los datos:
              datos['imagen'] = res;

              var urlImagenSubida;
              //Estamos usando como nombre de la imagen el nombrel del fichero.
              gapi.client.helloworld.alumnos.insertarAlumno2(datos).execute(function(resp){
                //Mostramos por consola la respuesta del servidor
                var salidaEjecucion=resp.message;
                console.log("Respuesta servidor insertarAlumno2: "+salidaEjecucion);
                console.log(salidaEjecucion);

                console.log("Respuesta servidor: "+salidaEjecucion);
                console.log(salidaEjecucion);

                if (salidaEjecucion == 'OK'){

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

          };



          fileReader.readAsDataURL(flowFile.file);
    });

  }
  var insertado = 0;
  $scope.submitForm = function(imagen){

    //Cuando el formulario es válido porque cumple con todas las especificaciones:
    if ($scope.formNuevoAlumno.$valid) {
       console.log('Formulario válido');
       console.log('Se progecede a guardar al alumno en la base de datos.')


       //Creamos un array con los elementos a enviar:
       var datos={
         //Aquí especificamos todos los datods del form que queremos que se envíen:
         'nombre':encode_utf8($scope.formNuevoAlumno.nombre.$modelValue),
         'apellidos':encode_utf8($scope.formNuevoAlumno.apellidos.$modelValue),
         'direccion':encode_utf8($scope.formNuevoAlumno.direccion.$modelValue),
         'localidad':encode_utf8($scope.formNuevoAlumno.localidad.$modelValue),
         'provincia':encode_utf8($scope.formNuevoAlumno.provincia.$modelValue),
         'fecha_nacimiento':$scope.formNuevoAlumno.fecha_nacimiento.$modelValue,
         'telefono':$scope.formNuevoAlumno.telefono.$modelValue,
         'dni':$scope.formNuevoAlumno.dni.$modelValue
       };
       console.log('Imprimiendo datos');
       console.log(datos);


       //Primero cargamos la imagen del usuario:
       console.log('Procesamiento de la imagen:');






       // ##### Si existe una imagen para subir ##### //
       //Si hay imágenes cargadas en ng-flow se llama a la función que las lee y llama a insertarAlumno.
       if (imagen.files.length!=0){
         console.log('Añadiendo imagen!!!!: ');
         insertarAlumno2ConImagen(imagen, datos);


       // ##### Si NO existe una imagen para subir ##### //
       }else{

                //Se llama al backend solo con los datos recogidos del formulario.

                gapi.client.helloworld.alumnos.insertarAlumno2(datos).execute(function(resp){
                  console.log('llamada a insertarAlumno2()');
                  //Mostramos por consola la respuesta del servidor
                  var salidaEjecucion=resp.message;
                  console.log("Respuesta servidor: "+salidaEjecucion);
                  console.log(salidaEjecucion);

                  if (salidaEjecucion == 'OK'){

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





       console.log('Imprimiendo datos 2');
       console.log(datos);

       console.log('IMAGEEEEENENNNN');
       console.log(imagen);
       console.log('Num Images');
       console.log(imagen.files.length);




       var salidaEjecucion;



    //   console.log('Formulario: ');
    //   console.log($scope.formNuevoAlumno);







     }
     else {
         //if form is not valid set $scope.addContact.submitted to true
         console.log('Formulario inválido');
         clase="uk-class-danger"
         $scope.formNuevoAlumno.submitted=true;
     };



  };
  /*
  console.log("Valor insertar: "+insertado);
  if(insertado == 1 ){
   $location.path("/estudiantes/main");
 }
 */




}); //Fin de controlador nuevo estudiante.




routerApp.controller('ControladorModificacionEstudiante', function($location, $scope, $stateParams){

  //Rescatamos el id de la url y la enviamos con el scope a la vista
  //$scope.id = $stateParams.estudianteID;
  $scope.id=$stateParams.estudianteID;

  /*
  Función que sube los datos del usuario junto a la imagen.
  */
  function modificacionUsuarioConNuevaImagen(datos, imagen){
    console.log('calling modificaiconUsuarioConNuevaImagen con datos e imagen')
    console.log(imagen)
    console.log(imagen.files)
    //Llamamos a la función que sube la imagen:
    //subirImagen($scope.file, 'caca');

    var urlImagenSubida="";

    angular.forEach(imagen.files, function(flowFile, i){
       var fileReader = new FileReader();
          var nombre = flowFile.file.name;

          fileReader.onload = function (event) {
            var uri = event.target.result;
              //$scope.imageStrings[i] = uri;

              var res = uri.slice(23);
              //console.log('Sending2 : ' + res);

              var urlImagenSubida;
              //Estamos usando como nombre de la imagen el nombrel del fichero.

                datos.imagen=res;

                gapi.client.helloworld.alumnos.modAlumnoCompleto2(datos).execute(function(resp){
                  //Mostramos por consola la respuesta del servidor
                  salidaEjecucion=resp.message;
                  console.log("Respuesta servidor: "+salidaEjecucion);
                  console.log(salidaEjecucion);

                   if (salidaEjecucion == 'OK'){

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







              console.log('salida¡')
              console.log(urlImagenSubida)

          };



          fileReader.readAsDataURL(flowFile.file);
    });

    //setTimeout(this, 5000);
    console.log('return urlImagenSubida: '+urlImagenSubida)
    return urlImagenSubida;
  }


  function modificacionUsuarioSimple(datos){
    gapi.client.helloworld.alumnos.modAlumnoCompleto2(datos).execute(function(resp){
      //Mostramos por consola la respuesta del servidor
      salidaEjecucion=resp.message;
      console.log("Respuesta servidor: "+salidaEjecucion);
      console.log(salidaEjecucion);

       if (salidaEjecucion == 'OK'){

         $.UIkit.notify("Alumno modificado con muchísimo éxito.", {status:'success'});
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


  //Pedimos al Gateway toda la informaicón del Alumno.
  gapi.client.helloworld.alumnos.getAlumno({'id':$stateParams.estudianteID}).execute(function(resp) {

    console.log("calling getAlumno with id: "+$stateParams.estudianteID);
    console.log(resp);
    if(resp.imagen=='NULL'){
      console.log('Imagen viene con null, vamos a eliminarla del bloque');
      delete resp.imagen;
      console.log(resp);
    };
    $scope.alumno = resp;
    console.log(resp.nombre);
    $scope.$apply();
    /*
    $scope.es=resp.alumno;
    //Tenemos que hacer esto para que se aplique scope ya que la llamada a la API está fuera de Angular
    $scope.$apply();
    */
  });


  var eliminacionImagen=false;

  $scope.eliminaImagen = function(){
    console.log('eliminaImagen');
    console.log($scope.alumno.imagen);
    if ($scope.alumno.imagen != null){
      console.log('!= null');
      $scope.alumno.imagen = null;
      eliminacionImagen = true;
    }
  };


  $scope.submitForm = function(imagen){

    console.log('imagen');
    console.log(imagen);

    //Lógica del formulario.

    //Cuando el formulario es válido porque cumple con todas las especificaciones:
    if ($scope.formModAlumno.$valid) {
       console.log('Formulario válido');
       console.log('Se progecede a guardar la modificación del alumno en la base de datos.')


       var datos={
         //Aquí especificamos todos los datods del form que queremos que se envíen:
         'nombre':encode_utf8($scope.formModAlumno.nombre.$modelValue),
         'apellidos':encode_utf8($scope.formModAlumno.apellidos.$modelValue),
         'direccion':encode_utf8($scope.formModAlumno.direccion.$modelValue),
         'localidad':encode_utf8($scope.formModAlumno.localidad.$modelValue),
         'provincia':encode_utf8($scope.formModAlumno.provincia.$modelValue),
         'fecha_nacimiento':$scope.formModAlumno.fecha_nacimiento.$modelValue,
         'telefono':$scope.formModAlumno.telefono.$modelValue,
         'dni':$scope.formModAlumno.dni.$modelValue,

         /*Como vamos a modificar un alumno tamién necesitamos su id (para identif. en la BD)
         y lo recogemos del paso de params como antes para conseguir todos sus datos.*/
         'id':$stateParams.estudianteID

       };

       console.log(datos);


       if (imagen.files.length!=0){
         console.log('Se ha añadido una imagen para modificar la del usuario (tuviera este o no)');

         //Entonces se envían los datos junto a la imagen a la funció que realiza la modificación con una nueva imagen.
         modificacionUsuarioConNuevaImagen(datos, imagen);


        }else{
          //No se ha añadido ninguna imagen desde el equipo, entonces:


          //1. Puede que si haya modificado la imagen eliminando la que tenía pero sin subir una nueva.
          if(eliminacionImagen){
            console.log('Se elimina la imagen del usuario que tenía y queda sin imagen.');

            //Entonces se llama al procedimiento que modifica el usuario en el BackEnd (sin que haya que subir una imagen nueva antes)
            //y cuando vea que lleva null si
            //el usuario tenía imagen anteriormente cargada, que lo comprobará, 1. la eliminará del servidor y 2. el
            //campo de imagen del usuario lo pondrá a null.

            //Se pone el valor de imagen del conjunto de datos a null.
            datos.imagen="ZGVs"; //ZGVs parámetro especial que es 'del' en base64 para hacer que se elimine en el server.
            modificacionUsuarioSimple(datos);



          //2. Puede que no haya modificado la imagen.
          }else{
            console.log('No se realizan cambios en la imagen del usuario');

            //Se llama al procedimiento que modifica el usuario sin que haya que subir una imagen nueva antes,
            // y en el Backend se verá que no se han hecho cambios en la url de la imagen del usuario y solo modificará
            // los campos de texto.

            console.log($scope.alumno);
            console.log(datos);
            datos.imagen = $scope.alumno.imagen;
            console.log('Después');
            console.log(datos);
            modificacionUsuarioSimple(datos);

          };

        };





       /*
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

            $.UIkit.notify("Alumno guardado con muchísimo éxito.", {status:'success'});
          }else{
            $.UIkit.notify("\""+salidaEjecucion+"\"", {status:'warning'});
          }

         $scope.$apply();
       });

       */



     }
     else {
         //if form is not valid set $scope.addContact.submitted to true
         console.log('Formulario inválido');
         clase="uk-class-danger"
         $scope.formNuevoAlumno.submitted=true;
     };



  }; //Fin submitForm function()




});

routerApp.controller('ControladorDetallesEstudiante', function($location, $scope, $stateParams){

  //Implementación de las acciones que se producen cuando el BOTÓN ELIMINAR se pulsa.
  $scope.delAlumno = function(){
    console.log("Pulsada confirmación eliminación alumno id: "+$stateParams.estudianteID)



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




  //Pedimos al Gateway toda la información del Alumno.
  gapi.client.helloworld.alumnos.getAlumno({'id':$stateParams.estudianteID}).execute(function(resp) {

    console.log("calling getAlumno with id: "+$stateParams.estudianteID);
    console.log(resp);
    if(resp.imagen=='NULL'){
      console.log('Imagen viene con null, vamos a eliminarla del bloque');
      delete resp.imagen;
      console.log(resp);
    };
    $scope.alumno = resp;
    console.log(resp.nombre);
    $scope.$apply();
    /*
    $scope.es=resp.alumno;
    //Tenemos que hacer esto para que se aplique scope ya que la llamada a la API está fuera de Angular
    $scope.$apply();
    */
  });

  /*
  ### Información extra del estudiante para el apartado de DATOS ACADÉMICOS ###
  */

  //Pedimos al gateway que nos diga todos los profesores que imparten clase a ese alumno.
  gapi.client.helloworld.alumnos.getProfesoresAlumno({'id':$stateParams.estudianteID}).execute(function(resp){
    console.log("Profesores del alumno: ");
    console.log(resp.profesores);
    //Enviamos al scope no toda la respuesta sino la lista de profesores que se espeara que contenga esta.
    $scope.profesores = resp.profesores;
    $scope.$apply();
  });

  //Pedimos al gateway que nos diga todos las asignaturas a las que está matriculado ese alumno.
  gapi.client.helloworld.alumnos.getAsignaturasAlumno({'id':$stateParams.estudianteID}).execute(function(resp){
    console.log("Asignaturas del alumno: ");
    console.log(resp.asignaturas);
    $scope.asignaturas = resp.asignaturas;
    $scope.$apply();
  });

  //Pedimos al gateway que nos diga todos las clases en las que está matriculado ese alumno.
  gapi.client.helloworld.alumnos.getClasesAlumno({'id':$stateParams.estudianteID}).execute(function(resp){
    console.log("Clases del alumno: ");
    console.log(resp.clases);
    $scope.clases = resp.clases;
    $scope.$apply();
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
    $location.path("/profesores/main");

  };

  //Rescatamos el id de la url y la enviamos con el scope a la vista
  //$scope.id = $stateParams.estudianteID;
  $scope.id=$stateParams.profesorID;
  console.log("ID profesor: "+$stateParams.profesorID);



  //Pedimos al Gateway toda la información del profesor.
  gapi.client.helloworld.profesores.getProfesor({'id':$stateParams.profesorID}).execute(function(resp) {
    console.log("calling getProfesor with id: "+$stateParams.profesorID);
    console.log(resp);
    $scope.profesor = resp;
    $scope.$apply();
  });

  /*
  ### Información extra del profesor para el apartado de DATOS ACADÉMICOS ###
  */

  //Pedimos al gateway que nos diga todos los alumnos a los que imparte clase es profesor.
  gapi.client.helloworld.profesores.getAlumnosProfesor({'id':$stateParams.profesorID}).execute(function(resp){
    console.log("Aumnos del profesor: ");
    console.log(resp.alumnos);
    //Enviamos al scope no toda la respuesta sino la lista de profesores que se espeara que contenga esta.
    $scope.estudiantes = resp.alumnos;
    $scope.$apply();
  });

  //Pedimos al gateway que nos diga todos las asignaturas que imparte el profesor.
  gapi.client.helloworld.profesores.getAsignaturasProfesor({'id':$stateParams.profesorID}).execute(function(resp){
    console.log("Asignaturas del profesor: ");
    console.log(resp.asignaturas);
    $scope.asignaturas = resp.asignaturas;
    $scope.$apply();
  });

  //Pedimos al gateway que nos diga todos las clases en las que imparte el profesor.
  gapi.client.helloworld.profesores.getClasesProfesor({'id':$stateParams.profesorID}).execute(function(resp){
    console.log("Clases del profesor: ");
    console.log(resp.clases);
    $scope.clases = resp.clases;
    $scope.$apply();
  });

});

routerApp.controller('ControladorNuevoProfesor', function ($scope) {
  /*
  Controlador que manejará los datos del formulario enviándolos al servidor.
  */
  $scope.submitForm = function(formData){


    //Lógica del formulario.

    //Cuando el formulario es válido porque cumple con todas las especificaciones:
    if ($scope.formNuevoAlumno.$valid) {
       console.log('Formulario válido');
       console.log('Se progecede a guardar al alumno en la base de datos.')

       var salidaEjecucion;

       console.log("llamada a addAlumno()")
       console.log($scope.alumno);



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

// #################################
// # Controladores de asignaturas  #
// #################################
routerApp.controller('ControladorListaAsignaturas', function ($scope) {
    /*
    Controlador que provee a la plantilla profesores-lista.html la lista simplificada de todos los profesores
    a trabés del API Gateway usando el método getProfesores()
    */


    gapi.client.helloworld.asignaturas.getAsignaturas().execute(function(resp) {
      console.log("recibido desde APIGATEWAY asignaturas.getAsignaturas(): ")
      console.log(resp.asignaturas);
      $scope.asignaturas=resp.asignaturas;
      $scope.$apply();
    });

});


routerApp.controller('ControladorNuevaAsignatura', function ($scope, $location){
  $scope.submitForm = function(formData){
    //Cuando el formulario es válido porque cumple con todas las especificaciones:
    if ($scope.formNuevaAsignatura.$valid) {
       console.log('Formulario válido');
       console.log('Se progecede a guardar la asignatura en la base de datos.')

       var salidaEjecucion;

       console.log("llamada a asginaturas.insertarAsignatura()")
       console.log($scope.alumno);



       gapi.client.helloworld.asignaturas.insertarAsignatura({
         //Aquí especificamos todos los datods del form que queremos que se envíen:
         'nombre':encode_utf8($scope.alumno.nombre),

       }
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
            $.UIkit.notify("Asignatura guardado con muchísimo éxito.", {status:'success'});
            $location.path("/asignaturas/main");
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

routerApp.controller('ControladorDetallesAsignatura', function($location, $scope, $stateParams){

  //Implementación de la acción del botón delAsignatura
  $scope.delAsignatura = function(){
    console.log("Pulsada confirmación asignatura alumno id: "+$stateParams.asignaturaID)



    gapi.client.helloworld.asignaturas.delAsignatura({'id':$stateParams.asignaturaID}).execute(function(resp){
      //Mostramos por consola la respuesta del servidor
      console.log("llamando a delAsignatura");
      console.log(resp.message);
      $scope.respuesta=resp.message;


      //El mensje no sale debido (en principio) a que cambiamos de pantall
      if (resp.message == 'OK'){
        /*
        Para que los notify de UIkit funcionen deben estar cargdos tanto el fichero de estilo como el javascript
        de este componente, esto lo hcemos en la plantilla (html)
        */
        $.UIkit.notify("Asignatura eliminado con éxito.", {status:'success'});
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

  console.log("ID asignatura: "+$stateParams.asignaturaID);



  //Pedimos al Gateway toda la informaicón de la asignatura.
  gapi.client.helloworld.asignaturas.getAsignatura({'id':$stateParams.asignaturaID}).execute(function(resp) {
    console.log("calling getAsignatura with id: "+$stateParams.asignaturaID);
    console.log(resp);
    $scope.asignatura = resp;
    console.log(resp.nombre);
    $scope.$apply();
  });

  /*
  ### Información extra de la asginatura ###
  */

  //Pedimos al gateway todos los alumnos matriculados en esa asignatura.
  gapi.client.helloworld.asignaturas.getAlumnosAsignatura({'id':$stateParams.asignaturaID}).execute(function(resp){
    console.log("Petición al API Gateway de alumnos matriculados en la asignatura "+$stateParams.asignaturaID);
    console.log(resp.alumnos);
    $scope.estudiantes = resp.alumnos;
    $scope.$apply();
  });

  //Pedimos al gateway todos los profesores que imparten esa asisnatura.
  gapi.client.helloworld.asignaturas.getProfesoresAsignatura({'id':$stateParams.asignaturaID}).execute(function(resp){
    console.log("Petición al APIG de los profesores que imparten la asignatura "+$stateParams.asignaturaID);
    console.log(resp.profesores);
    $scope.profesores = resp.profesores;
    $scope.$apply();
  });

  //Pedimos al gateway todos los clases en las que se imparte esa asisnatura.
  gapi.client.helloworld.asignaturas.getClasesAsignatura({'id':$stateParams.asignaturaID}).execute(function(resp){
    console.log("Petición al APIG de las clases en las que se imparten la asignatura "+$stateParams.asignaturaID);
    console.log(resp.clases);
    $scope.clases = resp.clases;
    $scope.$apply();
  });


}); //Fin controlador detalles asignatura

routerApp.controller('ControladorModificacionAsignatura', function($location, $scope, $stateParams){

  //Rescatamos el id de la url y la enviamos con el scope a la vista
  //$scope.id = $stateParams.estudianteID;
  $scope.id=$stateParams.asignaturaID;



  //Pedimos al Gateway toda la informaicón del Alumno.
  gapi.client.helloworld.asignaturas.getAsignatura({'id':$stateParams.asignaturaID}).execute(function(resp) {

    console.log("calling getAsignatura with id: "+$stateParams.asignaturaID);
    console.log(resp);
    $scope.asignatura = resp;
    console.log(resp.nombre);
    $scope.$apply();
    /*
    $scope.es=resp.alumno;
    //Tenemos que hacer esto para que se aplique scope ya que la llamada a la API está fuera de Angular
    $scope.$apply();
    */
  });


  $scope.submitForm = function(formData){

    console.log("Solicitud de formulario")

    //Cuando el formulario es válido porque cumple con todas las especificaciones:
    if ($scope.formModificacionAsignatura.$valid) {
       console.log('Formulario válido');
       console.log('Se progecede a guardar la modificación del alumno en la base de datos.')

       var salidaEjecucion;

       console.log("llamada a modAlumnoCompleto()")
       console.log($scope.alumno);


       gapi.client.helloworld.asignaturas.modAsignaturaCompleta({
         'id':$stateParams.asignaturaID,
         //asignatura.nombre se coge de la plantilla con la directiva ng-model así: ng-model="asignatura.nombre"
         'nombre':$scope.asignatura.nombre
       }).execute(function(resp){
         //Mostramos por consola la respuesta del servidor
         salidaEjecucion=resp.message;
         console.log("Respuesta servidor: "+salidaEjecucion);
         console.log(salidaEjecucion);

          if (salidaEjecucion == 'OK'){
            /*
            Para que los notify de UIkit funcionen deben estar cargdos tanto el fichero de estilo como el javascript
            de este componente, esto lo hcemos en la plantilla (html)
            */
            $.UIkit.notify("Asignatura guardada con muchísimo éxito.", {status:'success'});
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

// #################################
// # Controladores de clases       #
// #################################
routerApp.controller('ControladorListaClases', function ($scope) {
    /*
    Controlador que provee a la plantilla clases-lista.html la lista simplificada de todos las clases
    a trabés del API Gateway usando el método getClases()
    */


    gapi.client.helloworld.clases.getClases().execute(function(resp) {
      console.log("recibido desde APIGATEWAY clases.getClases(): ")
      var clases = resp.clases;
      console.log(resp.clases);

      //Vamos a crear una estructura a partir del resultado de la api para una mejor visualización en la interfaz.

      //Vamos a crear un vector por cada nivel de estudios, bach, eso, etc.. que venga en la lista.
      var niveles = new Array();

      //Cada nivel tiene cursos

      //Cada curso tiene grupos
      function Nivel(nivel){
        this.nivel=nivel;
      }

      nuevoNivel = new Nivel('Bachillerato');
      console.log(nuevoNivel.nivel);

      for(var i=0; i<clases.length; i++){

        console.log(clases[i].nivel);

        //Puede que sea mejor idea que sea el Gateway quien nos prepare la información como
        //la queremos para no tenga que hacer ese procesamiento el cliente.

      }

      console.log(niveles);

      $scope.clases=resp.clases;
      $scope.$apply();
    });

});

routerApp.controller('ControladorNuevaClase', function ($scope){
  $scope.submitForm = function(formData){
    //Cuando el formulario es válido porque cumple con todas las especificaciones:
    if ($scope.formNuevaClase.$valid) {
       console.log('Formulario válido');
       console.log('Se progecede a guardar la clase en la base de datos.')

       var salidaEjecucion;

       console.log("llamada a asginaturas.insertarAsignatura()")
       console.log($scope.alumno);


       gapi.client.helloworld.clases.insertarClase({
         'curso':$scope.clase.curso,
         'grupo':$scope.clase.grupo,
         'nivel':$scope.clase.nivel,
       }
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
            $.UIkit.notify("Asignatura guardado con muchísimo éxito.", {status:'success'});
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

routerApp.controller('ControladorModificacionClase', function($location, $scope, $stateParams){

  //Rescatamos el id de la url y la enviamos con el scope a la vista
  //$scope.id = $stateParams.estudianteID;
  $scope.id=$stateParams.claseID;
  console.log('claseID : '+$stateParams.claseID);
  console.log($stateParams);


  //Pedimos al Gateway toda la asignatura (esta información la podríamos ahorrar si viniera desde el otro controlador).
  gapi.client.helloworld.clases.getClase({'id':$stateParams.claseID}).execute(function(resp) {
    console.log("calling getClase with id: "+$stateParams.claseID);
    console.log('Datos recibidos: ')
    console.log(resp);
    $scope.clase = resp;
    $scope.$apply();
  });


  $scope.submitFormModAsignatura = function(formData){

    console.log("Solicitud de formulario")

    //Cuando el formulario es válido porque cumple con todas las especificaciones:
    if ($scope.formModificacionClase.$valid) {
       console.log('Formulario válido');
       console.log('Se progecede a guardar la modificación de la clase en la BD.')

       var salidaEjecucion;


       console.log('Datos de llamada:')
       console.log('id:'+$stateParams.claseID);
       console.log($scope.clase);


       gapi.client.helloworld.clases.modClaseCompleta({
         'id': $stateParams.claseID,
         'curso': $scope.clase.curso,
         'grupo': $scope.clase.grupo,
         'nivel': $scope.clase.nivel
       }).execute(function(resp){
         //Mostramos por consola la respuesta del servidor
         salidaEjecucion=resp.message;
         console.log("Respuesta servidor: "+salidaEjecucion);
         console.log(salidaEjecucion);

          if (salidaEjecucion == 'OK'){
            /*
            Para que los notify de UIkit funcionen deben estar cargdos tanto el fichero de estilo como el javascript
            de este componente, esto lo hcemos en la plantilla (html)
            */
            $.UIkit.notify("Clase modificada con muchísimo éxito.", {status:'success'});
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
         $scope.formModificacionClase.submitted=true;
     };



  };




});

routerApp.controller('ControladorDetallesClase', function($location, $scope, $stateParams, $window){

  //Función que pide al gateway la lista de todas la asignaturas del sistema.
  $scope.cargarAsignaturas = function(){
    console.log("llamada a cargarAsignaturas");
    gapi.client.helloworld.asignaturas.getAsignaturas().execute(function(resp){
      console.log("Petición al API Gateway la lista de todas las asignaturas: ");
      console.log(resp.asignaturas);
      $scope.asignaturas = resp.asignaturas;
      $scope.$apply();
    });
  };

  //Función que asocia una o varias asignaturas a una clase concreta ( como Francés e Inglés a 1AESO)
  $scope.asociar = function(){
    console.log('Llamada a asociar()');
    asignaturasSeleccionadas = [];
    //Recogemos las selecciones y las introducimos en un vector.
    angular.forEach($scope.asignaturas, function(asignatura){
      if (!!asignatura.selected) asignaturasSeleccionadas.push(asignatura.id);
    })
    //Mostramos las asignaturas que han sido seleccionadas
    console.log('Asignaturas seleccionadas');
    console.log(asignaturasSeleccionadas);
    console.log('Para la clase con id: '+$scope.clase.id);

    var salidaEjecucionCorrecta = true;

    //Recorremos todas las asignaturas seleccionadas y las asociamos a esta clase como una especificación de cada asignatura.
    for(var i=0; i<asignaturasSeleccionadas.length; i++){
      gapi.client.helloworld.asociaciones.insertaAsociacion({'id_clase':$scope.clase.id, 'id_asignatura':asignaturasSeleccionadas[i]}).execute(function(resp){
        console.log('llamando a insertarAsociacion');
        console.log(resp.message);
        if (resp.message!= 'OK'){
          salidaEjecucionCorrecta = false;
        }
        console.log('Var de control salidaEjecucionCorrecta: '+salidaEjecucionCorrecta);
      });
    }

    if (salidaEjecucionCorrecta){
      /*
      Para que los notify de UIkit funcionen deben estar cargdos tanto el fichero de estilo como el javascript
      de este componente, esto lo hcemos en la plantilla (html)
      */
      $.UIkit.notify("Asignatura añadida con éxito.", {status:'success'});
    }else{
      $.UIkit.notify("\""+salidaEjecucion+"\"", {status:'warning'});
    }
  };


  $scope.delImparte = function(idImparte){
    console.log('Calling delImparte with params: idImparte '+idImparte);
    gapi.client.helloworld.impartes.delImparte({'id':idImparte} ).execute(function(resp){
      console.log('Peticion al API Gateway de la eliminacion de una tupla en la tabla Imparte');
      console.log(resp.message);
      var respuesta=resp.message;
      if (respuesta == 'OK'){
        $.UIkit.notify("Relacion eliminada con muchísimo éxito.", {status:'success'});
      }else{
        $.UIkit.notify("\""+respuesta+"\"", {status:'warning'});
      }
    });
  }

  $scope.delMatricula = function(idMatricula){
    console.log('Calling delMatricula with params: idMatricula '+idMatricula);
    gapi.client.helloworld.matriculas.delMatricula({'id':idMatricula} ).execute(function(resp){
      console.log('Peticion al API Gateway de la eliminacion de una tupla en la tabla Matricula');
      console.log(resp.message);
      var respuesta=resp.message;
      if (respuesta == 'OK'){
        $.UIkit.notify("Alumno desmatriculado con muchísimo éxito.", {status:'success'});
      }else{
        $.UIkit.notify("\""+respuesta+"\"", {status:'warning'});
      }
    });
  }

  //Función que pide al gateway la lista de todos los profesores del sistema.
  $scope.cargarProfesores = function(param){
    console.log('llamada a cargarProfesores y seteo del param idAsociacion: '+param);
    $scope.idAsociacion=param;
    gapi.client.helloworld.profesores.getProfesores().execute(function(resp){
      console.log('Petición al API Gateway de la lista de todos los profesores');
      console.log(resp.profesores);
      $scope.profesores = resp.profesores;
      $scope.$apply();
    });
  };

  $scope.cargarAlumnos = function(param){
    console.log('llamada a cargarAlumnos');
    //Hacemos lo mismo que con los profesores
    $scope.idAsociacion=param;
    gapi.client.helloworld.alumnos.getAlumnos().execute(function(resp){
        console.log('Petición al API Gateway de la lista de todos los alumnos');
        console.log(resp.alumnos);
        $scope.alumnos = resp.alumnos;
        $scope.$apply();
    });
  };


  /*Función que asigna un profesor a una asociación (asignatura-clase). para que imparta una especificación de una asignatura en concreto en una clase concreta
  como Literatura a 3ºB-ESO */
  $scope.asignar = function(){
    console.log('Llamada a asignar()');

    console.log('Obtención valor idAsociacion: '+$scope.idAsociacion);

    profesoresSeleccionados = [];
    //Recogemos las selecciones y las introducimos en un vector.
    angular.forEach($scope.profesores, function(profesor){
      if (!!profesor.selected) profesoresSeleccionados.push(profesor.id);
    })
    //Mostramos las profesor que han sido seleccionadas
    console.log('Profesores seleccionados');
    console.log(profesoresSeleccionados);
    console.log('Para la asociacion con id: '+$scope.idAsociacion);

    var salidaEjecucionCorrecta = true;

    //Recorremos todas las profesor seleccionadas y las asociamos a esta clase como una especificación de cada asignatura.
    for(var i=0; i<profesoresSeleccionados.length; i++){
      gapi.client.helloworld.impartes.insertarImparte({'id_asociacion':$scope.idAsociacion, 'id_profesor':profesoresSeleccionados[i]}).execute(function(resp){
        console.log('llamando a insertarImparte');
        console.log(resp.message);
        if (resp.message!= 'OK'){
          salidaEjecucionCorrecta = false;
        }
        console.log('Var de control salidaEjecucionCorrecta: '+salidaEjecucionCorrecta);

      });
    }



    if (salidaEjecucionCorrecta){
      /*
      Para que los notify de UIkit funcionen deben estar cargdos tanto el fichero de estilo como el javascript
      de este componente, esto lo hcemos en la plantilla (html)
      */
      $.UIkit.notify("Asignación realizada con éxito.", {status:'success'});
    }else{
      $.UIkit.notify("\""+salidaEjecucion+"\"", {status:'warning'});
    }


    //Antes de terminar recargamos la página:
    /*
    Ahora mismo lo que hace es recargar toda la aplicación, pero lo que queremos es que recarge solo la página en la que estamos con este
    controlador.
    */
    $window.location.reload();



  };


  $scope.matricular = function(){
    console.log('Llamada a matricular()');

    console.log('Asociacion: '+$scope.idAsociacion);

    /*El procedimiento es el mismo que se hace con los profesores en asignar, recorrer la lista de los seleccionados y
    llamar a la api tantas veces como profesores tengamos.
    */

    alumnosSeleccionados = [];
    //Recogemos las selecciones y las introducimos en un vector.
    angular.forEach($scope.alumnos, function(alumno){
      if (!!alumno.selected) alumnosSeleccionados.push(alumno.id);
    })
    //Mostramos las profesor que han sido seleccionadas
    console.log('Alumnos seleccionados');
    console.log(alumnosSeleccionados);
    console.log('Para la asociacion con id: '+$scope.idAsociacion);


    //Recorremos todas las profesor seleccionadas y las asociamos a esta clase como una especificación de cada asignatura.
    for(var i=0; i<alumnosSeleccionados.length; i++){
      gapi.client.helloworld.matriculas.insertarMatricula({'id_asociacion':$scope.idAsociacion, 'id_alumno':alumnosSeleccionados[i]}).execute(function(resp){
        console.log('llamando a insertarMatricula');
        console.log(resp.message);
      });
    }

  }


  //Implementación de la acción del botón delAsignatura
  $scope.delClase = function(clase){
    console.log("Pulsada confirmación eliminación clase con id: "+clase.id)


    gapi.client.helloworld.clases.delClase({'id':$stateParams.claseID}).execute(function(resp){
      //Mostramos por consola la respuesta del servidor
      console.log("llamando a delClase");
      console.log(resp.message);
      $scope.respuesta=resp.message;


      //El mensje no sale debido (en principio) a que cambiamos de pantall
      if (resp.message == 'OK'){
        /*
        Para que los notify de UIkit funcionen deben estar cargdos tanto el fichero de estilo como el javascript
        de este componente, esto lo hcemos en la plantilla (html)
        */
        $.UIkit.notify("Clase eliminado con éxito.", {status:'success'});
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
  $scope.id=$stateParams.claseID;

  console.log("ID clase: "+$stateParams.claseID);



  //Pedimos al Gateway toda la informaicón de la clase.
  gapi.client.helloworld.clases.getClase({'id':$stateParams.claseID}).execute(function(resp) {
    console.log("Petición al API Gateway de información de la clase con ID:  "+$stateParams.claseID);
    console.log(resp);
    $scope.clase = resp;
    console.log(resp.clase);
    $scope.$apply();
  });

  /*
  ### Información extra de la asginatura ###
  */


  //Pedimos al gateway todos los alumnos matriculados en esa clase (de cualquier asignatura)
  gapi.client.helloworld.clases.getAlumnosClase({'id':$stateParams.claseID}).execute(function(resp){
    console.log("Petición al API Gateway de alumnos matriculados en la clase con ID:  "+$stateParams.claseID);
    console.log(resp.alumnos);
    $scope.estudiantes = resp.alumnos;
    $scope.$apply();
  });

  //Pedimos al gateway todos los profesores que imparten a esa clase (de cualquier asignatura)
  gapi.client.helloworld.clases.getProfesoresClase({'id':$stateParams.claseID}).execute(function(resp){
    console.log("Petición al API Gateway de profesores que imparten en la clase con ID:  "+$stateParams.claseID);
    console.log(resp.profesores);
    $scope.profesores = resp.profesores;
    $scope.$apply();
  });

  //Pedimos al gateway todas las asignaturas que se imparten en esa clase.
  gapi.client.helloworld.clases.getAsignaturasClase({'id':$stateParams.claseID}).execute(function(resp){
    console.log("Petición al API Gateway de los asignaturas que se imparten en la clase con ID:  "+$stateParams.claseID);
    console.log(resp.asignaturas);
    $scope.asignaturas = resp.asignaturas;
    $scope.$apply();
  });

  /*
  ### Información extra MÁS específica ###
  */

  /*Pedimos al gateway todas las asociaciones que se imparten en esa clase, es decir todas las asignaturas que se imparten en
  esa clase pero no para saber la información general, como Francés que nos llevará a la información de la asignatura sino
  para saber por ejemplo en esa clase de 1AESO en la asginatura de Matematicas (eso es una asociación entre asignatura y clase)
  quiés es el profesor y quienes los alumnos, ya que pueden exisitir alumnos matriculados en 1AESO que den Métodos de la Ciencia
  y otros que den Religión. Ámbos grupos pertenecen a 1AESO pero cada uno está matriculado auna especificación de esas asignaturas
  en esta clase en concreto que además imparte un profesor en concreto.
  */


  //Creamos un array donde guardamos todos los bloques de información que nos vengan
  var listaAsociacionesCompleta = new Array();

  //Pedimos todas las asociaciones (especificaciones de asignaturas) que se dan para  la clase y toda la información de cada una.
  gapi.client.helloworld.clases.getAsociacionesClase({'id':$stateParams.claseID}).execute(function(resp){
    console.log("Petición al API Gateway de las asociaciones (especificaciones) de la asignaturas que se imparten en esta clase");

    //Guardamos la respuesta.
    listaAsociaciones = resp.asociaciones;

    //Una asociación es asignatura en clase. (inglés en 1ºABach)

    //Ahora por cada asociación que tenga esta clase vamos a pedir todos sus datos:
    for(var i=0; i<listaAsociaciones.length; i++){
      console.log(listaAsociaciones[i].nombreAsignatura);

      gapi.client.helloworld.asociaciones.getAsociacionCompleta({'id':listaAsociaciones[i].id_asociacion}).execute(function(resp){
        console.log('Info asociación completa: ');
        console.log(resp);
        //Añadimos cada bloque de info al array:
        console.log('AsociacionCompletaObtenida: ')
        listaAsociacionesCompleta.push(resp);
        console.log(listaAsociacionesCompleta);
        $scope.$apply();
      });

    }

    //Metemos la info obtenida en el scope para poder usarla
    console.log('listaAsociacionesCompleta:');
    console.log(listaAsociacionesCompleta);
    $scope.asociaciones=listaAsociacionesCompleta;

    $scope.$apply();



  });












}); //Fin controlador detalles asignatura

// ###################################
// # Controlador de página de perfil #
// ###################################

routerApp.controller('ControladorProfilePage', function($scope){

  console.log($scope.currentUser);

  //Pedimos al Gateway toda la informaicón del usuario, en este caso del profesor, ya que es el único
  //tipo de usuario por el momento que tiene página de perfil y acceso al sistema como tal.

  //Obtenemos los datos del profesor en cuestión usando el id que está almacenado en la información de sesión
  //en la variable currentUser
  gapi.client.helloworld.profesores.getProfesor({'id': $scope.currentUser.id}).execute(function(resp) {
    console.log("calling profesores.getProfesor with id: 1");
    console.log(resp);
    $scope.profesor = resp;
    $scope.$apply();
  });

});

// ###########################################
// # Controladores de Control de Estudiantes #
// ###########################################
routerApp.controller('ControladorCE-asistencia-historico', function($scope){

  $scope.resumenes='Muchos resumenes';

});

routerApp.controller('ControladorCE-asistencia-nuevo', function($scope, $location, $rootScope){


  //LLamamos al APIG para mostrar todas las asociaciones (Asignatura-Clase) que imparter clase cierto profesor.
  //El id del profesor lo cojemos los valores del usuario logueado.
  gapi.client.helloworld.profesores.getAsociacionesProfesor({'id': '1'}).execute(function(resp){
    console.log('calling profesor.getAsociacionesProfesor with id 1');
    console.log(resp);
    $scope.asociaciones = resp.asociaciones;
    $scope.$apply();
  });


  /*
  Tendremos que crear un método que al pulsar sobre una asocaicion la grabe en el scope y
  entonces llame a la página de la realización del CE-asistencia y donde se lea allí.
  Si se hiciera pasándolo por la url entonces cualquier usuario podría poner la url y acceder
  a la realización de un CE-asistencia sobre los alumnos de una asociacion que puede no ser la suya,
  para evitar esto también podriamos comprobar si ese usuario puede hacer ese CE en ese idasociacon
  comprobando si pertenece a sus asociaciones pero sería tener que llamar otra vez a getAsociacionesProfesor
  en otro controlador.
  */

  $scope.goCE = function(idAsociacion) {
    console.log('ID_Asociacion en goCE: '+idAsociacion);
    $rootScope.id_asociacion=idAsociacion;

    $location.path("/cear");
    //grabar el id en el scope

    //ir a la realización del CE
  };


});

routerApp.controller('ControladorCE-asistencia-realizacion', function($scope, $rootScope){


  console.log('realización de control de estudiantes con: ')
  console.log($rootScope.id_asociacion);


  gapi.client.helloworld.asociaciones.getAlumnos({'id': $rootScope.id_asociacion}).execute(function(resp){
    alumnos= resp.alumnos;
    //Asignamos ciertos valors por defecto a todos los estudiantes:
    for(var i=0; i < alumnos.length; ++i){
      //El alumno ha venido a clase:
      alumnos[i].asistencia=1;
      //El alumno ha sido puntual:
      alumnos[i].retraso=0;
      //Por tanto no necesita justificante de retraso:
      alumnos[i].retrasoJustificado=0;
      //Ha traido el uniforme
      alumnos[i].uniforme=1;
    }
    console.log(alumnos);
    //Una vez modificados los pasamos a la vista a través del scope
    $scope.alumnos = alumnos;
    //console.log(resp.alumnos);
    $scope.$apply();
  });



  /*
  var a1 = new Object();
  a1.nombre="Marco Aureliio ";
  a1.apellidos="Barrancos Martinez";
  a1.id=1;
  a1.asistencia=1;
  a1.retraso=10;
  a1.retrasoJustificado=0;
  a1.uniforme=1;

  var a2 = new Object();
  a2.nombre="Antonia ";
  a2.apellidos="San Juan";
  a2.id=2;
  a2.asistencia=1;
  a2.retraso=0;
  a2.retrasoJustificado=0;
  a2.uniforme=1;

  var alumnos = [];
  alumnos.push(a1);
  alumnos.push(a2);

  $scope.alumnos=alumnos;
 */

  $scope.anotarAsistencia = function(idAlumno, asistencia){
    console.log('anotarAsistencia with line '+idAlumno+'  asistencia: '+asistencia);
    //Ahora buscamos al alumno con id=idAlumno y marcar el campo asistencia al valor que nos pase la función.
    //No podemos usar filter porque devuelve un array de objetos, no su índice. Más info en: https://developer.mozilla.org/es/docs/Web/JavaScript/Referencia/Objetos_globales/Array/filter
    for(var i=0; i < alumnos.length; ++i){
      console.log(alumnos[i].id);
      if (alumnos[i].id==idAlumno){
        //Cuando encontramos el alumnos que es ponemos su asisntecia como nos dice la UI
        alumnos[i].asistencia=asistencia;
      }
    }
  }

  $scope.justificarRetraso = function(idAlumno){
    console.log('justificarRetraso with line '+idAlumno);
    for(var i=0; i < alumnos.length; ++i){
      console.log(alumnos[i].id);
      if (alumnos[i].id==idAlumno){
        //Cuando encontramos el alumnos que es ponemos su justificacion como nos dice la UI
        if(alumnos[i].retrasoJustificado==0){
          alumnos[i].retrasoJustificado=1;
        }else{
          alumnos[i].retrasoJustificado=0;
        }

      }
    }
  }

  $scope.anotarUniforme = function(idAlumno, uniforme){
    console.log('anotarUniforme with line '+idAlumno+'  uniforme: '+uniforme);
    //Ahora buscamos al alumno con id=idAlumno y marcar el campo uniforme al valor que nos pase la función.
    //No podemos usar filter porque devuelve un array de objetos, no su índice. Más info en: https://developer.mozilla.org/es/docs/Web/JavaScript/Referencia/Objetos_globales/Array/filter
    for(var i=0; i < alumnos.length; ++i){
      console.log(alumnos[i].id);
      if (alumnos[i].id==idAlumno){
        //Cuando encontramos el alumnos que es ponemos su asisntecia como nos dice la UI
        alumnos[i].uniforme=uniforme;
      }
    }
  }

  $scope.anotarRetraso = function(idAlumno){
    console.log('AnotarREtraso');
    console.log('Retraso del estudiante id: '+idAlumno);
    //Con cada llamada se aumenta el retraso del estudiante en 10 min: 0 -> 10 -> 20 o más.
    //Primero buscamos al alumno:
    for(var i=0; i < alumnos.length; ++i){
      if (alumnos[i].id==idAlumno){
        console.log('encontrado');
        console.log(alumnos[i].retraso);
        //Vamos cambiando entre las tres opciones de retraso que puede haber.
        if(alumnos[i].retraso==0){
          console.log('Cambiando a 10');
          alumnos[i].retraso=10;
        }else if(alumnos[i].retraso==10){
          alumnos[i].retraso=20;
        }else if(alumnos[i].retraso==20){
          alumnos[i].retraso=0;
        }
      }
    }
  }

  $scope.isSelected = false;
      $scope.toggleButtonState = function(){
          $scope.isSelected = !$scope.isSelected;
      }

  $scope.activeButton = function() {
      console.log('PRESS BUTTON');
      $scope.isActive = !$scope.isActive;
    }
  //$scope.alumnos = 'lista de alumnos rechulones';
  $scope.date = new Date();

});
