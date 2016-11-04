angular.module('students')
    .factory("StudentsService",
        function($resource) {

         var restPath = 'http://localhost:8001/entities/student/';

         return $resource(restPath + ':id', {id: '@studentId'}, {
             'getSubjects': {
                 method: 'GET',
                 url: restPath + ':id' + '/subject',
                 isArray: true
             },

             'update': {method: 'PUT'},

             'getClasses': {
                 method: 'GET',
                 url: restPath + ':id' + '/class',
                 isArray: true
             }
             });
        });
