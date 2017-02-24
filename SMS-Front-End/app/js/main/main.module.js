//Main module of app

//angular.module("main", ["teaching"]);


//ngMaterial -> Module to use angular material directives.
//teaching -> Teaching module


angular.module('main', ['ngMaterial', 'ui.router', 'teachers',
    'students', 'subjects', 'classes', 'associations', 'imparts', 'enrollments',
    'attendanceControls', 'marks', 'discipline', 'ngResource', 'angularMoment']);

angular.module('main').config(function ($stateProvider, $urlRouterProvider) {

    $urlRouterProvider.otherwise('/home');

    $stateProvider

        .state('home', {url: '/home', templateUrl: 'app/views/home.html'})

        /*####################
         ## Teaching  Module ##
         ####################*/

        .state('teachers', {url: '/teachers', templateUrl: 'app/views/teaching/teachers/teachersList.html'})
        .state('teachersProfile', {
            url: '/teachers/:teacherId',
            templateUrl: 'app/views/teaching/teachers/teachersProfile.html'
        })

        .state('students', {url: '/students', templateUrl: 'app/views/teaching/students/studentsList.html'})
        .state('studentsProfile', {
            url: '/students/:studentId',
            templateUrl: 'app/views/teaching/students/studentsProfile.html'
        })

        .state('subjects', {url: '/subjects', templateUrl: 'app/views/teaching/subjects/subjectsList.html'})
        .state('subjectsProfile', {
            url: '/subjects/:subjectId',
            templateUrl: 'app/views/teaching/subjects/subjectsProfile.html'
        })

        .state('classes', {url: '/grupos', templateUrl: 'app/views/teaching/classes/classesList.html'})
        .state('classesProfile', {
            url: '/grupos/:classId',
            templateUrl: 'app/views/teaching/classes/classesProfile.html'
        })


        /*###########################
         ## Students Control Module ##
         ###########################*/

        .state('attendanceControls', {
            url: '/controles_asistencia',
            templateUrl: 'app/views/studentsControl/attendanceControls/attendanceControlsList.html'
        })
        .state('attendanceControlProfile', {
            url: '/controles_asistencia/:acId',
            templateUrl: 'app/views/studentsControl/attendanceControls/attendanceControl.html'
        })
        .state('newAttendanceControl', {
            url: '/controles_asistencia/nuevo/:associationId',
            templateUrl: 'app/views/studentsControl/attendanceControls/attendanceControl.html'
        })

        .state('marks', {
                url: '/notas',
                templateUrl: 'app/views/studentsControl/marks/marks.html'
            })

        .state('discipline', {
                url: '/discipline',
                templateUrl: 'app/views/studentsControl/discipline/discipline.html'
            })

});


angular.module('main').config(function ($mdThemingProvider) {

    $mdThemingProvider.definePalette('specialpalette', {
        'pastelGreen': 'A7FF84',
        'pastelRed': 'EB7B78',
        'gray': '9e9e9e',
        'pastelOrange': 'EBA534',
        '50': 'ffebee',
        '100': 'ffcdd2',
        '200': 'ef9a9a',
        '300': 'e57373',
        '400': 'ef5350',
        '500': 'f44336',
        '600': 'e53935',
        '700': 'd32f2f',
        '800': 'c62828',
        '900': 'b71c1c',
        'A100': 'ff8a80',
        'A200': 'ff5252',
        'A400': 'ff1744',
        'A700': 'd50000',
        'contrastDefaultColor': 'light',


        'contrastDarkColors': ['50', '100',
            '200', '300', '400', 'A100'],
        'contrastLightColors': undefined
    });
    $mdThemingProvider.theme('specialtheme')
        .primaryPalette('specialpalette')

    $mdThemingProvider.theme('default')
        .primaryPalette('indigo');
})

angular.module('main').controller('AppCtrl', function ($scope, $mdSidenav, $mdMedia, $mdToast) {
    $scope.toggleSidenav = function (menu) {
        $mdSidenav(menu).toggle();
    }

    $scope.$mdMedia = $mdMedia;

    $scope.toast = function (message) {
        var toast = $mdToast.simple().content('You clicked ' + message).position('bottom right');
        $mdToast.show(toast);
    };
    $scope.toastList = function (message) {
        var toast = $mdToast.simple().content('You clicked ' + message + ' having selected ' + $scope.selected.length + ' item(s)').position('bottom right');
        $mdToast.show(toast);
    };
    $scope.selected = [];
    $scope.toggle = function (item, list) {
        var idx = list.indexOf(item);
        if (idx > -1) list.splice(idx, 1);
        else list.push(item);
    };
    $scope.data = {
        title: 'SMS',
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
            }, {
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
                actions: [
                    {
                        name: 'Control Asistencia',
                        icon: 'done_all',
                        link: '.attendanceControls'
                    },
                    {
                        name: 'Notas',
                        icon: 'library_books',
                        link: '.marks'
                    },
                    {
                        name: 'Disciplina',
                        icon: 'report',
                        link: '.discipline'
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