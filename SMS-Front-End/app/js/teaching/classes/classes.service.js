angular.module('classes')
    .factory("ClassesService",
        function($resource, globalService) {



         var restPath = 'http://'+globalService.defaultMicroServicesURL+'/entities/class/';

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
             'nested_delete':{
                 method: 'DELETE',
                 url: restPath + ':id/:a/:b'  // Example: /entities/class/1/student/1
             },
             'getStudents': {
                 method: 'GET',
                 url: restPath + ':id' + '/student',
                 isArray: true
             },

             'update': {method: 'PUT'},
         });

        });
