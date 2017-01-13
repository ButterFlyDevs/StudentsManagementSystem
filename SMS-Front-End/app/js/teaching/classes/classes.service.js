angular.module('classes')
    .factory("ClassesService",
        function($resource) {

         var restPath = 'http://localhost:8001/entities/class/';

         return $resource(restPath + ':id', {id: '@classId', a:'a', b:'b'}, {

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
             'nested_delete':{
                 method: 'DELETE',
                 url: restPath + ':id/:a/:b'

             },
             'getStudents': {
                 method: 'GET',
                 url: restPath + ':id' + '/student',
                 isArray: true
             },

             'update': {method: 'PUT'},
         });

        });
