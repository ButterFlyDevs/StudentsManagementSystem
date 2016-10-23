angular.module('students')
    .factory("StudentsService",
        function($resource) {

         var restPath = 'http://localhost:8001/entities/student/';

         return $resource(restPath + ':id', {id: '@_id'}, {
             'getSubjects': {
                 method: 'GET',
                 url: restPath + ':id' + '/subject',
                 isArray: true
             },
             'getClasses': {
                 method: 'GET',
                 url: restPath + ':id' + '/class',
                 isArray: true
             }
             });
        });
