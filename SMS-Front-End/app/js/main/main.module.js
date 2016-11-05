//Main module of app

//angular.module("main", ["teaching"]);


//ngMaterial -> Module to use angular material directives.
//teaching -> Teaching module


angular.module('main', ['ngMaterial', 'ui.router', 'teachers', 'students', 'subjects', 'classes', 'associations', 'imparts', 'ngResource', 'angularMoment']);



angular.module('main').config(function($stateProvider, $urlRouterProvider){

    $urlRouterProvider.otherwise('/home');

    $stateProvider

        .state('home', { url: '/home', templateUrl: 'app/views/home.html'})

        .state('teachers', { url: '/teachers', templateUrl: 'app/views/teaching/teachers/teachersList.html'})
        .state('teachersProfile', {url: '/teachers/:teacherId', templateUrl: 'app/views/teaching/teachers/teachersProfile.html'})

        .state('students', { url: '/students', templateUrl: 'app/views/teaching/students/studentsList.html'})
        .state('studentsProfile', {url: '/students/:studentId', templateUrl: 'app/views/teaching/students/studentsProfile.html'})

        .state('subjects', { url: '/subjects', templateUrl: 'app/views/teaching/subjects/subjectsList.html'})
        .state('subjectsProfile', {url: '/subjects/:subjectId', templateUrl: 'app/views/teaching/subjects/subjectsProfile.html'})

        .state('classes', { url: '/classes', templateUrl: 'app/views/teaching/classes/classesList.html'})
        .state('classesProfile', {url: '/classes/:classId', templateUrl: 'app/views/teaching/classes/classesProfile.html'})

  })




angular.module('main').config(function($mdThemingProvider) {
  $mdThemingProvider.theme('default').primaryPalette('indigo');
})

angular.module('main').controller('AppCtrl', function($scope, $mdSidenav, $mdMedia, $mdToast) {
  $scope.toggleSidenav = function(menu) {
    $mdSidenav(menu).toggle();
  }

  $scope.$mdMedia = $mdMedia;

  $scope.toast = function(message) {
    var toast = $mdToast.simple().content('You clicked ' + message).position('bottom right');
    $mdToast.show(toast);
  };
  $scope.toastList = function(message) {
    var toast = $mdToast.simple().content('You clicked ' + message + ' having selected ' + $scope.selected.length + ' item(s)').position('bottom right');
    $mdToast.show(toast);
  };
  $scope.selected = [];
  $scope.toggle = function(item, list) {
    var idx = list.indexOf(item);
    if (idx > -1) list.splice(idx, 1);
    else list.push(item);
  };
  $scope.data = {
    title: 'Dashboard',
    user: {
      name: 'Susana',
      icon: 'face'
    },
    toolbar: {
      buttons: [{
        name: 'Button 1',
        icon: 'add',
        link: 'Button 1'
      }],
      menus: [{
        name: 'Menu 1',
        icon: 'message',
        width: '4',
        actions: [{
          name: 'Action 1',
          message: 'Action 1',
          completed: true,
          error: true
        }, {
          name: 'Action 2',
          message: 'Action 2',
          completed: false,
          error: false
        }, {
          name: 'Action 3',
          message: 'Action 3',
          completed: true,
          error: true
        }]
      }]
    },

    //Define the sidenav in floating left menu
    sidenav: {
      sections: [{
        name: 'Principal',
        link: '.home'
        },{
        name: 'Docencia',
        expand: false,
        actions: [{
          name: 'Profesores',
          icon: 'settings',
          link: '.teachers'
        }, {
          name: 'Estudiantes',
          icon: 'settings',
          link: '.students'
        }, {
          name: 'Asignaturas',
          icon: 'settings',
          link: '.subjects'
        }, {
          name: 'Grupos',
          icon: 'settings',
          link: '.classes'
        }]
      }, {
        name: 'Control Estudiantes',
        expand: false,
        actions: [{
          name: 'Action 3',
          icon: 'settings',
          link: 'Action 3'
        }]
      }]
    },
    content: {
      lists: [{
        name: 'List 1',
        menu: {
          name: 'Menu 1',
          icon: 'settings',
          width: '4',
          actions: [{
            name: 'Action 1',
            message: 'Action 1',
            completed: true,
            error: true
          }]
        },
        items: [{
          name: 'Item 1',
          description: 'Description 1',
          link: 'Item 1'
        }, {
          name: 'Item 2',
          description: 'Description 2',
          link: 'Item 2'
        }, {
          name: 'Item 3',
          description: 'Description 3',
          link: 'Item 3'
        }]
      }]
    }
  }
});