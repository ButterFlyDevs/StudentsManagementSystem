//This is the module of teaching ("docencia").
var teachingModule = angular.module("teaching", ["teachers"])
    .controller('teachingController',
                ['$scope', function($scope) { $scope.greeting = 'Hola!'; }]
               );

