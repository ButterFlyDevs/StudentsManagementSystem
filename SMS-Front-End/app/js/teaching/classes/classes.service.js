angular.module('classes')
    .factory("ClassesService",
        function($resource) {

         var restPath = 'http://localhost:8001/entities/class/';

         return $resource(restPath + ':id', {id: '@classId'}, {

             'getTeaching': {
                 method: 'GET',
                 url: restPath + ':id' + '/teaching',
                 isArray: true
             },

             'getReport': {
                 method: 'GET',
                 url: restPath + ':id' + '/report'
             },
             'delete':{
                 method: 'DELETE',
                 url: restPath + ':id' + '?action=dd' // Delete dependencies also.
             },
             'getStudents': {
                 method: 'GET',
                 url: restPath + ':id' + '/student',
                 isArray: true
             },

             'update': {method: 'PUT'},
         });

        });
