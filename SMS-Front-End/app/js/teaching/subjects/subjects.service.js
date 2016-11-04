angular.module('subjects')
    .factory("SubjectsService",
        function($resource) {

         var restPath = 'http://localhost:8001/entities/subject/';

         return $resource(restPath + ':id', {id: '@subjectId'}, {
             'getTeachers': {
                 method: 'GET',
                 url: restPath + ':id' + '/teacher',
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
