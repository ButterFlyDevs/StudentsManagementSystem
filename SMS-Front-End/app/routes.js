//Fichero de rutas de la aplicación.
// ############# ENRUTADOR #################################### //

routerApp.config(function($stateProvider, $urlRouterProvider, USER_ROLES) {
/*

Configura el enrutamiento de todas las vistas de la web. Implementa a que URLs
responden que vistas y mediante que controladores. Estos controladores son las FUNCIONES
que piden los datos donde proceda y los cargan en las vistas donde serán usados y vicesversa (se cargan
de la vista y se usan).
*/

    $urlRouterProvider.otherwise('/login');

    $stateProvider


       //Configuración de la pantalla de login
       .state('login', {
         url: '/login',
         templateUrl:'login.html',

         data: {
           authorizedRoles: [USER_ROLES.all]
         }
       })


       //Perfil
       .state('profile', {
         url: '/profile',
         templateUrl:'profile.html',
         controller: 'ControladorProfilePage',

         data: {
           authorizedRoles: [USER_ROLES.admin]
         }
       })



       //Configura la URL principal
       .state('#',{
         url:'/home',
         templateUrl:'main.html',
         data: {
           authorizedRoles: [USER_ROLES.admin]
         }
       })

        /*Definición de VISTAS ANIDADAS, dentro de una vista general que es la de estudiantes se incrustan
        a su derecha todas las subsecciones distintas. Así estudiantes.html define la plantilla general y dentro de
        ella está una sección en la que se cargarán las subpartes estudiantes.<subpartes>
        Ver estudiantes.html.
        En este caso esta vista no tiene controlador porque no la necesita.
        */
        .state('estudiantes', {
            url: '/estudiantes',
            templateUrl: 'estudiantes/estudiantes.html',
            //El rol de autorización se hereda a los hijos de esta vista.
            data: {
              authorizedRoles: [USER_ROLES.admin]
            }
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
             templateUrl: 'profesores/profesores.html',
             data: {
               authorizedRoles: [USER_ROLES.admin]
             }
         })
         .state('profesores.main', {
             url: '/main',
             templateUrl: 'profesores/profesores-main.html',
         })
         .state('profesores.list', {
              url: '/list',
              templateUrl: 'profesores/profesores-lista.html',
              controller: 'ControladorListaProfesores'
          })
          .state('profesores.detalles-profesor',{
            url: '/detalle/:profesorID',
            templateUrl: 'profesores/profesores-detalle.html',
            controller: 'ControladorDetallesProfesor'
          })
          .state('profesores.nuevo', {
              url: '/nuevo',
              //Podemos meter directamente texto desde aquí
              //template: 'I could sure use a drink right now.'
              templateUrl: 'profesores/profesores-nuevo.html',
              controller: 'ControladorNuevoProfesor'
          })



          //CONTROLADORES DE ASIGNATURAS

           .state('asignaturas', {
               url: '/asignaturas',
               templateUrl: 'asignaturas/asignaturas.html',
               data: {
                 authorizedRoles: [USER_ROLES.admin]
               }
           })
           .state('asignaturas.main', {
               url: '/main',
               templateUrl: 'asignaturas/asignaturas-main.html',
           })
           .state('asignaturas.list', {
                url: '/list',
                templateUrl: 'asignaturas/asignaturas-lista.html',
                controller: 'ControladorListaAsignaturas'
            })
            .state('asignaturas.detalles-asignatura',{
              url: '/detalle/:asignaturaID',
              templateUrl: 'asignaturas/asignaturas-detalle.html',
              controller: 'ControladorDetallesAsignatura'
            })
            .state('asignaturas.modificacion-asignatura',{
              url: '/modificacion/:asignaturaID',
              templateUrl: 'asignaturas/asignaturas-modificacion.html',
              controller: 'ControladorModificacionAsignatura'
            })
            .state('asignaturas.nuevo', {
                url: '/nuevo',
                //Podemos meter directamente texto desde aquí
                //template: 'I could sure use a drink right now.'
                templateUrl: 'asignaturas/asignaturas-nuevo.html',
                controller: 'ControladorNuevaAsignatura'
            })


            //CONTROLADORES DE CLASES

             .state('clases', {
                 url: '/clases',
                 templateUrl: 'clases/clases.html',
                 data: {
                   authorizedRoles: [USER_ROLES.admin]
                 }
             })
             .state('clases.main', {
                 url: '/main',
                 templateUrl: 'clases/clases-main.html',
             })
             .state('clases.list', {
                  url: '/list',
                  templateUrl: 'clases/clases-lista.html',
                  controller: 'ControladorListaClases'
              })
              .state('clases.detalles-clase',{
                url: '/detalle/:claseID',
                templateUrl: 'clases/clases-detalle.html',
                controller: 'ControladorDetallesClase'
              })
              .state('clases.modificacion-clase',{
                url: '/modificacion/:claseID',
                templateUrl: 'clases/clases-modificacion.html',
                controller: 'ControladorModificacionClase'
              })
              .state('clases.nueva', {
                  url: '/nuevo',
                  //Podemos meter directamente texto desde aquí
                  //template: 'I could sure use a drink right now.'
                  templateUrl: 'clases/clases-nuevo.html',
                  controller: 'ControladorNuevaClase'
              })

              //Controladores de la sección de control de estudiantes.
              .state('control-estudiantes', {
                  url: '/control-estudiantes',
                  templateUrl: 'controlEstudiantes/control-estudiantes.html',
                  data: {
                    authorizedRoles: [USER_ROLES.admin]
                  }
              })
              .state('control-estudiantes.main', {
                  //La url se conforma extendiendo la del padre: /control-estudiantes/main
                  url: '/main',
                  templateUrl: 'controlEstudiantes/control-estudiantes-main.html',
              })

              .state('control-estudiantes.asistencia-inicio', {
                  url: '/asistencia-inicio',
                  templateUrl: 'controlEstudiantes/control-estudiantes-asistencia-inicio.html',
              })
              .state('control-estudiantes.asistencia-historico', {
                  url: '/asistencia-historico',
                  templateUrl: 'controlEstudiantes/control-estudiantes-asistencia-historico.html',
                  controller: 'ControladorCE-asistencia-historico',
              })
              .state('control-estudiantes.asistencia-nuevo', {
                  url: '/asistencia-nuevo',
                  templateUrl: 'controlEstudiantes/control-estudiantes-asistencia-nuevo.html',
                  controller: 'ControladorCE-asistencia-nuevo',
              })

              .state('control-estudiantes-asistencia-realizacion', {
                  url: '/cear',
                  templateUrl: 'controlEstudiantes/control-estudiantes-asistencia-realizacion.html',
                  data: {
                    authorizedRoles: [USER_ROLES.all]
                  },
                  controller: 'ControladorCE-asistencia-realizacion',
              })


        // ABOUT PAGE AND MULTIPLE NAMED VIEWS =================================
        .state('about', {
            // we'll get to this in a bit
            url:'/about',
            template: 'This is an another page',
            data: {
              authorizedRoles: [USER_ROLES.admin]
            }
        });

});//Final de config.
